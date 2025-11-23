from openpyxl import load_workbook
from apps.productos.models import Producto
from decimal import Decimal, InvalidOperation
from django.db import transaction


def procesar_cargue_productos(archivo):
    """
    Procesa el archivo Excel de productos y crea registros nuevos.
    Si encuentra un producto existente o hay errores, cancela todo el cargue.
    """

    resultados = {
        'exitosos': 0,
        'fallidos': 0,
        'errores': []
    }

    try:
        wb = load_workbook(archivo)
        ws = wb.active

        productos_a_crear = []

        for fila_num, fila in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                if not any(fila):
                    continue

                referencia = str(fila[0]).strip() if fila[0] else None
                articulo = str(fila[1]).strip() if fila[1] else None
                precio_costo = fila[2]
                precio_venta = fila[3]
                linea = str(fila[4]).strip().upper() if fila[4] else None
                descripcion = str(fila[5]).strip() if fila[5] else None

                if not referencia:
                    resultados['errores'].append(f"Fila {fila_num}: Referencia vacía")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                if not articulo:
                    resultados['errores'].append(f"Fila {fila_num}: Artículo vacío para referencia '{referencia}'")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                if not linea:
                    resultados['errores'].append(f"Fila {fila_num}: Línea vacía para referencia '{referencia}'")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                if not descripcion:
                    resultados['errores'].append(f"Fila {fila_num}: Descripción vacía para referencia '{referencia}'")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                if Producto.objects.filter(referencia=referencia).exists():
                    resultados['errores'].append(f"Fila {fila_num}: El producto con referencia '{referencia}' ya existe")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                try:
                    precio_costo = Decimal(str(precio_costo))
                    precio_venta = Decimal(str(precio_venta))
                except (InvalidOperation, ValueError, TypeError):
                    resultados['errores'].append(f"Fila {fila_num}: Precios inválidos para {referencia}")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                if precio_costo < 0 or precio_venta < 0:
                    resultados['errores'].append(f"Fila {fila_num}: Los precios deben ser positivos para {referencia}")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                lineas_validas = ['HOMBRE', 'DAMA', 'UNISEX']
                if linea not in lineas_validas:
                    resultados['errores'].append(f"Fila {fila_num}: Línea '{linea}' no válida para {referencia}. Valores válidos: {', '.join(lineas_validas)}")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                productos_a_crear.append(Producto(
                    referencia=referencia,
                    articulo=articulo,
                    precio_costo=precio_costo,
                    precio_venta=precio_venta,
                    linea=linea,
                    descripcion=descripcion
                ))

            except Exception as e:
                resultados['errores'].append(f"Fila {fila_num}: Error procesando - {str(e)}")
                resultados['fallidos'] += 1
                wb.close()
                return resultados

        wb.close()

        if productos_a_crear:
            try:
                with transaction.atomic():
                    Producto.objects.bulk_create(productos_a_crear)
                    resultados['exitosos'] = len(productos_a_crear)
            except Exception as e:
                resultados['errores'].append(f"Error al guardar productos en la base de datos: {str(e)}")
                resultados['fallidos'] = len(productos_a_crear)
                return resultados

    except Exception as e:
        resultados['errores'].append(f"Error al leer el archivo: {str(e)}")
        resultados['fallidos'] += 1

    return resultados
