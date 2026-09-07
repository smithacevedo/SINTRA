#!/usr/bin/env python3
"""
Script para actualizar Productos: fijar `referencia_externa=False` donde actualmente es NULL.
Uso:
  python scripts/set_referencia_externa_false.py [--apply]

Por defecto hace un dry-run y muestra ejemplos; pasar `--apply` para aplicar los cambios.
"""
import os
import sys
import argparse

# Añadir la raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Ajustar según el módulo de settings de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from apps.productos.models import Producto


def main():
    parser = argparse.ArgumentParser(description='Fija referencia_externa=False donde es NULL')
    parser.add_argument('--apply', action='store_true', help='Aplica los cambios en la base de datos')
    parser.add_argument('--preview', type=int, default=10, help='Número de filas de ejemplo a mostrar en dry-run')
    args = parser.parse_args()

    qs = Producto.objects.filter(referencia_externa__isnull=True)
    total = qs.count()
    print(f"Productos con referencia_externa IS NULL: {total}")
    if total == 0:
        print("No hay registros para actualizar.")
        return

    if not args.apply:
        print("Modo dry-run. Ejecuta con --apply para aplicar los cambios.")
        print(f"Mostrando hasta {args.preview} ejemplos:")
        for p in qs[:args.preview]:
            try:
                print(f"- ID={p.pk} referencia={p.referencia}")
            except Exception:
                print(f"- ID={p.pk} (error leyendo referencia)")
        return

    # Aplicar actualización en bloque
    updated = qs.update(referencia_externa=False)
    print(f"Registros actualizados: {updated}")


if __name__ == '__main__':
    main()
