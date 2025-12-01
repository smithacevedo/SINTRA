from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CargaMasivaForm
from .procesadores import procesar_cargue_clientes, procesar_cargue_productos, procesar_cargue_proyectos


@login_required
def lista_cargues(request):
    """
    Vista que muestra la lista de tipos de cargues masivos disponibles
    """
    cargues = [
        {'id': 'productos', 'nombre': 'Cargar Productos'},
        {'id': 'clientes', 'nombre': 'Cargar Clientes'},
        {'id': 'proyectos', 'nombre': 'Cargar Proyectos'},
        {'id': 'ordenes_compra', 'nombre': 'Cargar Órdenes de Compra'},
        {'id': 'proveedores', 'nombre': 'Cargar Proveedores'},
        {'id': 'despachos', 'nombre': 'Cargar Despachos'},
        {'id': 'remisiones', 'nombre': 'Cargar Remisiones'},
    ]

    context = {
        'cargues': cargues,
        'segment': 'cargues_masivos'
    }

    return render(request, 'cargues_masivos/lista_cargues.html', context)


@login_required
def cargue_detalle(request, tipo_cargue):
    """
    Vista para realizar un cargue masivo específico
    """

    tipos_validos = {
        'productos': 'Cargar Productos',
        'clientes': 'Cargar Clientes',
        'proyectos': 'Cargar Proyectos',
        'ordenes_compra': 'Cargar Órdenes de Compra',
        'proveedores': 'Cargar Proveedores',
        'despachos': 'Cargar Despachos',
        'remisiones': 'Cargar Remisiones',
    }

    if tipo_cargue not in tipos_validos:
        messages.error(request, 'Tipo de cargue no válido')
        return redirect('cargues_masivos:lista_cargues')

    nombre_cargue = tipos_validos[tipo_cargue]

    if request.method == 'POST':
        form = CargaMasivaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']

            # CARGUE DE PRODUCTOS
            if tipo_cargue == 'productos':
                resultados = procesar_cargue_productos(archivo)

                if resultados['exitosos'] > 0:
                    messages.success(request, f"Cargue exitoso: {resultados['exitosos']} productos creados")

                if resultados['fallidos'] > 0 and len(resultados['errores']) > 0:
                    # Mostrar todos los errores
                    for error in resultados['errores']:
                        messages.error(request, error)

            # CARGUE DE CLIENTES
            elif tipo_cargue == 'clientes':
                resultados = procesar_cargue_clientes(archivo)
                if resultados['exitosos'] > 0:
                    messages.success(request, f"Cargue exitoso: {resultados['exitosos']} clientes creados")
                if resultados['fallidos'] > 0 and len(resultados['errores']) > 0:

                    for error in resultados['errores']:
                        messages.error(request, error)

            # CARGUE DE PROYECTOS
            elif tipo_cargue == 'proyectos':
                resultados = procesar_cargue_proyectos(archivo)

                if resultados['exitosos'] > 0:
                    messages.success(request, f"Cargue exitoso: {resultados['exitosos']} proyectos creados")

                if resultados['fallidos'] > 0 and len(resultados['errores']) > 0:
                    for error in resultados['errores']:
                        messages.error(request, error)

            else:
                # Otros tipos de cargue
                messages.info(request, f'Procesamiento de {nombre_cargue} no disponible.')

            return redirect('cargues_masivos:lista_cargues')
    else:
        form = CargaMasivaForm()

    archivos_ejemplo = {
        'productos': 'ejemplo_productos.xlsx',
        'clientes': 'ejemplo_clientes.xlsx',
        'proyectos': 'ejemplo_proyectos.xlsx',
        'ordenes_compra': 'ejemplo_ordenes_compra.xlsx',
        'proveedores': 'ejemplo_proveedores.xlsx',
        'despachos': 'ejemplo_despachos.xlsx',
        'remisiones': 'ejemplo_remisiones.xlsx',
    }

    context = {
        'form': form,
        'tipo_cargue': tipo_cargue,
        'nombre_cargue': nombre_cargue,
        'archivo_ejemplo': archivos_ejemplo.get(tipo_cargue, None),
        'segment': 'cargues_masivos'
    }

    return render(request, 'cargues_masivos/cargue_detalle.html', context)
