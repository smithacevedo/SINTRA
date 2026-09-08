#!/usr/bin/env python
"""Script único que ejecuta la operación completa: crear despachos pendientes,
adjuntar/crear remisiones con PDF genérico y marcar órdenes finalizadas según
la lógica de negocio. Colócalo en `scripts/` y ejecútalo desde el repo.

Ejemplos:
  python scripts/close_orders_finalize.py --dry-run
  python scripts/close_orders_finalize.py --force --limit 10
"""
import os
import sys
import argparse
import base64


def find_pdf(pdf_path_arg):
    if pdf_path_arg:
        if not os.path.exists(pdf_path_arg):
            raise FileNotFoundError(f'Archivo PDF no encontrado: {pdf_path_arg}')
        return pdf_path_arg

    # Buscar candidato por defecto en apps/templates/PDF/factura_generica_finalizada.pdf
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, '..'))
    candidates = [
        os.path.join(repo_root, 'apps', 'templates', 'PDF', 'factura_generica_finalizada.pdf'),
        os.path.join(repo_root, 'apps', 'templates', 'PDF', 'factura_generica_finalizada.pdf'),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    raise FileNotFoundError('No se encontró PDF por defecto. Pasa --pdf-path con la ruta al PDF genérico.')


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, '..'))

    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    try:
        import django
    except Exception:
        print('Error: Django no está disponible. Activa el virtualenv e instala dependencias.', file=sys.stderr)
        raise

    django.setup()

    from django.conf import settings
    from apps.ordenes_compra.models import OrdenCompra
    from apps.remisiones.models import Remision, DetalleRemision
    from apps.despachos.models import Despacho

    parser = argparse.ArgumentParser(description='Close orders: create dispatches, attach PDF, close remissions, finalize orders')
    parser.add_argument('--dry-run', action='store_true', help='Simular sin aplicar cambios')
    parser.add_argument('--pdf-path', type=str, help='Ruta al PDF genérico')
    parser.add_argument('--no-dispatch', action='store_true', help='No crear despachos automáticos')
    parser.add_argument('--force', action='store_true', help='Forzar marcar órdenes como finalizadas')
    parser.add_argument('--limit', type=int, default=0, help='Límite de órdenes a procesar (0 = todas)')

    args = parser.parse_args()

    dry_run = args.dry_run
    no_dispatch = args.no_dispatch
    force = args.force
    limit = args.limit or 0

    try:
        pdf_path = find_pdf(args.pdf_path)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_name = os.path.basename(pdf_path)

    qs = OrdenCompra.objects.all().order_by('id')
    total = qs.count()
    if limit > 0:
        qs = qs[:limit]

    processed = 0
    created_remisiones = 0
    updated_remisiones = 0

    dispatch_pending = not no_dispatch

    for orden in qs:
        print(f'Procesando Orden id={orden.id} codigo={orden.codigo_oc} cliente={orden.cliente}')
        remisiones = list(orden.remisiones.all())
        created_dispatches = []

        if dispatch_pending:
            for prod in orden.productos.all():
                pendiente = prod.pendiente
                if pendiente and pendiente > 0:
                    if dry_run:
                        print(f"[DRY-RUN] Se crearía Despacho para ProductoSolicitado id={prod.id} cantidad={pendiente}")
                    else:
                        desp = Despacho(producto_solicitado=prod, cantidad=pendiente, reintegro=False, created_by=None)
                        desp.save()
                        created_dispatches.append(desp)
                        print(f'Creado Despacho id={desp.id} para ProductoSolicitado id={prod.id} cantidad={pendiente}')

        if not remisiones:
            if dry_run:
                print(f'[DRY-RUN] Se crearía Remision para Orden id={orden.id}')
            else:
                rem = Remision(orden=orden, estado_facturacion='cerrado', factura_base64=pdf_b64, factura_nombre=pdf_name)
                rem.save()
                created_remisiones += 1
                print(f'Remision creada id={rem.id} para Orden id={orden.id}')
                if created_dispatches:
                    for desp in created_dispatches:
                        det = DetalleRemision(remision=rem, despacho=desp)
                        det.save()
                        print(f'DetalleRemision creada id={det.id} vinculando Remision id={rem.id} y Despacho id={desp.id}')
        else:
            for rem in remisiones:
                if dry_run:
                    print(f'[DRY-RUN] Se actualizaría Remision id={rem.id} (estado_facturacion -> cerrado, adjuntar pdf)')
                else:
                    rem.factura_base64 = pdf_b64
                    rem.factura_nombre = pdf_name
                    rem.estado_facturacion = 'cerrado'
                    rem.save()
                    updated_remisiones += 1
                    print(f'Remision id={rem.id} actualizada.')
                    if created_dispatches:
                        for desp in created_dispatches:
                            det = DetalleRemision(remision=rem, despacho=desp)
                            det.save()
                            print(f'DetalleRemision creada id={det.id} vinculando Remision id={rem.id} y Despacho id={desp.id}')

        nuevo_estado = orden.actualizar_estado
        if dry_run:
            print(f'[DRY-RUN] Orden id={orden.id} estado calculado={nuevo_estado}')
            if force:
                print('[DRY-RUN] --force presente: se marcaría como finalizada de todas formas')
        else:
            if nuevo_estado == 'finalizada' or force:
                orden.estado_orden = 'finalizada'
                orden.save()
                print(f'Orden id={orden.id} marcada como finalizada.')
            else:
                print(f'Orden id={orden.id} NO se marca como finalizada (estado calculado={nuevo_estado}). Usa --force para forzar).')

        processed += 1

    print(f'Procesadas {processed} órdenes (total en BD: {total}). Remisiones creadas: {created_remisiones}, actualizadas: {updated_remisiones}')


if __name__ == '__main__':
    main()
