from openpyxl import load_workbook
from apps.clientes.models import Clientes
from apps.productos.models import Producto
from decimal import Decimal, InvalidOperation
from django.db import transaction
from cities_light.models import City
from apps.proyectos.models import Proyectos


def procesar_cargue_productos(archivo):
    """
    Procesa el archivo Excel de productos y crea registros nuevos.
    Si encuentra un producto existente o hay errores, cancela todo el cargue.
    Autor: Jeison Acevedo
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

def procesar_cargue_clientes(archivo):
    """
    Procesa el archivo Excel de clientes y crea registros nuevos.
    Si encuentra un cliente existente o hay errores, cancela todo el cargue.
    Autor: Jeison Acevedo
    """

    wb = load_workbook(archivo)
    ws = wb.active
    resultados = {
        'exitosos': 0,
        'fallidos': 0,
        'errores': []
    }
    clientes_a_crear = []
    try:
        for fila_num, fila in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                if not any(fila):
                    continue
                nombre_cliente = str(fila[0]).strip() if fila[0] else None
                email_cliente = str(fila[1]).strip() if fila[1] else None
                nombre_contacto = str(fila[2]).strip() if fila[2] else None
                telefono_contacto = str(fila[3]).strip() if fila[3] else None
                email_contacto = str(fila[4]).strip() if fila[4] else None
                direccion = str(fila[5]).strip() if fila[5] else None
                ciudad_name = str(fila[6]).strip() if fila[6] else None
                tiene_proyectos = str(fila[7]).strip().upper() if fila[7] else None

                if not nombre_cliente:
                    resultados['errores'].append(f"Fila {fila_num}: Nombre de cliente vacío")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados
                if Clientes.objects.filter(nombre_cliente=nombre_cliente).exists():
                    resultados['errores'].append(f"Fila {fila_num}: El cliente '{nombre_cliente}' ya existe")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados
                ciudad_obj = City.objects.filter(name=ciudad_name).first() if ciudad_name else None
                if not ciudad_obj:
                    resultados['errores'].append(f"Fila {fila_num}: Ciudad '{ciudad_name}' no encontrada")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados
                if tiene_proyectos not in ['SI', 'NO']:
                    resultados['errores'].append(f"Fila {fila_num}: Valor de proyectos inválido '{tiene_proyectos}' (debe ser SI o NO)")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados
                tiene_proyectos_bool = True if tiene_proyectos == 'SI' else False

                clientes_a_crear.append(Clientes(
                    nombre_cliente=nombre_cliente,
                    email_cliente=email_cliente,
                    nombre_contacto=nombre_contacto,
                    telefono_contacto=telefono_contacto,
                    email_contacto=email_contacto,
                    direccion_cliente=direccion,
                    ciudad_cliente=ciudad_obj,
                    tiene_proyectos=tiene_proyectos_bool
                ))
            except Exception as e:
                resultados['errores'].append(f"Fila {fila_num}: Error procesando - {str(e)}")
                resultados['fallidos'] += 1
                wb.close()
                return resultados
        wb.close()
        if clientes_a_crear:
            try:
                with transaction.atomic():
                    Clientes.objects.bulk_create(clientes_a_crear)
                    resultados['exitosos'] = len(clientes_a_crear)
            except Exception as e:
                resultados['errores'].append(f"Error al guardar clientes en la base de datos: {str(e)}")
                resultados['fallidos'] = len(clientes_a_crear)
                return resultados
    except Exception as e:
        resultados['errores'].append(f"Error al leer el archivo: {str(e)}")
        resultados['fallidos'] += 1
    return resultados

def procesar_cargue_proyectos(archivo):
    """
    Procesa el archivo Excel de proyectos y crea registros nuevos.
    Si encuentra un proyecto existente o hay errores, cancela todo el cargue.
    Autor: Jeison Acevedo
    """

    wb = load_workbook(archivo)
    ws = wb.active
    resultados = {
        'exitosos': 0,
        'fallidos': 0,
        'errores': []
    }
    proyectos_a_crear = []
    try:
        for fila_num, fila in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                if not any(fila):
                    continue
                nombre_cliente = str(fila[0]).strip().lower() if fila[0] else None
                ciudad_name = str(fila[1]).strip().lower() if fila[1] else None
                nombre_proyecto = str(fila[2]).strip() if fila[2] else None
                email_proyecto = str(fila[3]).strip() if fila[3] else None
                nombre_contacto = str(fila[4]).strip() if fila[4] else None
                telefono_contacto = str(fila[5]).strip() if fila[5] else None
                email_contacto = str(fila[6]).strip() if fila[6] else None
                direccion = str(fila[7]).strip() if fila[7] else None

                campos = [nombre_cliente, ciudad_name, nombre_proyecto, email_proyecto, nombre_contacto, telefono_contacto, email_contacto, direccion]
                if not all(campos):
                    resultados['errores'].append(f"Fila {fila_num}: Algún campo está vacío")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                cliente_obj = None
                for c in Clientes.objects.filter(tiene_proyectos=True):
                    if c.nombre_cliente and c.nombre_cliente.strip().lower() == nombre_cliente:
                        cliente_obj = c
                        break
                if not cliente_obj:
                    resultados['errores'].append(f"Fila {fila_num}: Cliente '{nombre_cliente}' no existe o no tiene proyectos habilitados")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                ciudad_obj = None
                for city in City.objects.all():
                    if city.name and city.name.strip().lower() == ciudad_name:
                        ciudad_obj = city
                        break
                if not ciudad_obj:
                    resultados['errores'].append(f"Fila {fila_num}: Ciudad '{ciudad_name}' no encontrada")
                    resultados['fallidos'] += 1
                    wb.close()
                    return resultados

                proyectos_a_crear.append(Proyectos(
                    cliente=cliente_obj,
                    ciudad_proyecto=ciudad_obj,
                    nombre_proyecto=nombre_proyecto,
                    email_proyecto=email_proyecto,
                    nombre_contacto=nombre_contacto,
                    telefono_contacto=telefono_contacto,
                    email_contacto=email_contacto,
                    direccion_proyecto=direccion
                ))
            except Exception as e:
                resultados['errores'].append(f"Fila {fila_num}: Error procesando - {str(e)}")
                resultados['fallidos'] += 1
                wb.close()
                return resultados
        wb.close()
        if proyectos_a_crear:
            try:
                with transaction.atomic():
                    Proyectos.objects.bulk_create(proyectos_a_crear)
                    resultados['exitosos'] = len(proyectos_a_crear)
            except Exception as e:
                resultados['errores'].append(f"Error al guardar proyectos en la base de datos: {str(e)}")
                resultados['fallidos'] = len(proyectos_a_crear)
                return resultados
    except Exception as e:
        resultados['errores'].append(f"Error al leer el archivo: {str(e)}")
        resultados['fallidos'] += 1
    return resultados
