#!/usr/bin/env python
"""
Script: recibir_ordenes_excluyendo_2026.py

Recibe (registra despachos y crea remisiones) para todas las `OrdenCompra`
except aquellas cuya `fecha_solicitud` pertenezca al año 2026.

Uso:
  python scripts/recibir_ordenes_excluyendo_2026.py --dry-run
  python scripts/recibir_ordenes_excluyendo_2026.py --apply --user admin

Precaución: ejecutar primero en entorno de pruebas o con `--dry-run`.
"""
import os
import sys
import argparse
from datetime import date, datetime
from django.db import transaction
from django.contrib.auth import get_user_model

# Ensure project root is on sys.path and Django is configured before importing models
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
try:
    import django
    django.setup()
except Exception:
    # If django isn't available in this environment, allow imports to fail later when run in the project env
    pass

from apps.ordenes_compra.models import OrdenCompra
from apps.remisiones.models import Remision, DetalleRemision
from apps.despachos.models import Despacho
from django.utils import timezone


def recibir_ordenes_excluyendo_ano(ano_excluir=2026, dry_run=True, username=None):
    User = get_user_model()
    user = None
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"Usuario '{username}' no encontrado. Continuando con created_by=None")

    qs = OrdenCompra.objects.exclude(fecha_solicitud__year=ano_excluir).order_by('fecha_solicitud')

    resumen = {
        'ordenes_iteradas': 0,
        'ordenes_procesadas': 0,
        'despachos_creados': 0,
        'remisiones_creadas': 0,
    }

    for orden in qs:
        resumen['ordenes_iteradas'] += 1
        productos = list(orden.productos.select_related('producto').all())
        despachos_para_orden = []

        for ps in productos:
            pendiente = ps.pendiente
            if pendiente and pendiente > 0:
                despachos_para_orden.append((ps, pendiente))

        if not despachos_para_orden:
            # nada por despachar en esta orden
            continue

        print(f"Procesando Orden {orden.codigo_oc} (fecha: {orden.fecha_solicitud}) - elementos a despachar: {len(despachos_para_orden)}")

        if dry_run:
            resumen['ordenes_procesadas'] += 1
            resumen['despachos_creados'] += sum(p for (_, p) in despachos_para_orden)
            continue

        # ejecutar creación dentro de transacción por orden
        # La función puede recibir un valor global de fecha de recibido a aplicar.
        # Si `received_dt` está en el scope (definido por el main), úsalo; sino crear objetos con valores por defecto.
        with transaction.atomic():
            created_despachos = []
            created_despachos_pks = []
            for ps, cantidad in despachos_para_orden:
                despacho_kwargs = {
                    'producto_solicitado': ps,
                    'cantidad': cantidad,
                    'created_by': user
                }
                despacho = Despacho.objects.create(**despacho_kwargs)
                created_despachos.append(despacho)
                created_despachos_pks.append(despacho.pk)

            # Si se proporcionó una fecha de recibido, forzarla en BD para los despachos recién creados
            if 'received_dt' in globals() and globals().get('received_dt') is not None and created_despachos_pks:
                Despacho.objects.filter(pk__in=created_despachos_pks).update(fecha_despacho=globals().get('received_dt'))

            # crear remisión y detalles (permitir fecha personalizada)
            rem = Remision.objects.create(orden=orden)
            if 'received_dt' in globals() and globals().get('received_dt') is not None:
                # forzar fecha_remision en BD
                Remision.objects.filter(pk=rem.pk).update(fecha_remision=globals().get('received_dt'))
                rem.refresh_from_db()

            for d in created_despachos:
                DetalleRemision.objects.create(remision=rem, despacho=d)

            # actualizar estado de la orden según la lógica del modelo
            orden.estado_orden = orden.actualizar_estado
            orden.save()

            resumen['ordenes_procesadas'] += 1
            resumen['despachos_creados'] += len(created_despachos)
            resumen['remisiones_creadas'] += 1

    return resumen


def main():
    parser = argparse.ArgumentParser(description='Recibir órdenes (excluye año) y crear remisiones')
    parser.add_argument('--dry-run', action='store_true', help='Mostrar resumen sin crear objetos')
    parser.add_argument('--apply', action='store_true', help='Aplicar los cambios en la base de datos')
    parser.add_argument('--user', help='Nombre de usuario para asignar como created_by en despachos')
    parser.add_argument('--exclude-year', type=int, default=datetime.now().year, help='Año a excluir (por defecto: año actual)')
    parser.add_argument('--received-date', type=str, default='2025-12-31', help='Fecha de recibido a aplicar a despachos/remisiones (YYYY-MM-DD). Por defecto: 2025-12-31')

    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print('Indica --dry-run o --apply. Por defecto se recomienda --dry-run para pruebas.')
        return

    dry = args.dry_run or not args.apply

    # Parsear fecha de recibido si la proporcionan y guardarla en una variable global `received_dt`
    global received_dt
    received_dt = None
    if args.received_date:
        try:
            parsed_date = datetime.strptime(args.received_date, '%Y-%m-%d').date()
            # usamos la medianoche como time component
            dt = datetime.combine(parsed_date, datetime.min.time())
            # hacer aware si settings usan TZ
            try:
                received_dt = timezone.make_aware(dt)
            except Exception:
                received_dt = dt
        except Exception as e:
            print(f"Formato de --received-date inválido: {e}. Use YYYY-MM-DD")
            return

    resumen = recibir_ordenes_excluyendo_ano(ano_excluir=args.exclude_year, dry_run=dry, username=args.user)

    print('\n--- Resumen ---')
    print(f"Órdenes iteradas: {resumen['ordenes_iteradas']}")
    print(f"Órdenes con elementos a despachar: {resumen['ordenes_procesadas']}")
    print(f"Despachos (filas) creados: {resumen['despachos_creados']}")
    print(f"Remisiones creadas: {resumen['remisiones_creadas']}")


if __name__ == '__main__':
    main()
