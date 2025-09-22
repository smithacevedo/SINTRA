from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.ordenes_compra.models import OrdenCompra, ProductoSolicitado
from .models import Despacho
from .forms import DespachoForm


def buscar_orden(request):
    codigo_oc = ""
    if request.method == "POST":
        codigo_oc = request.POST.get("codigo_oc", "").strip()
        if codigo_oc:
            try:
                orden = OrdenCompra.objects.get(codigo_oc=codigo_oc)
                messages.success(request, f"Orden {codigo_oc} encontrada exitosamente.")
                return redirect("consultar_orden", codigo_oc=orden.codigo_oc)
            except OrdenCompra.DoesNotExist:
                messages.error(request, f"La orden con código {codigo_oc} no existe.")
        else:
            messages.warning(request, "Debe ingresar un código de orden.")
    return render(request, "despachos/buscar_orden.html", {"codigo_oc": codigo_oc})


def consultar_orden(request, codigo_oc):
    try:
        orden = OrdenCompra.objects.get(codigo_oc=codigo_oc)
        messages.success(request, f"Mostrando detalle de la orden {codigo_oc}.")
    except OrdenCompra.DoesNotExist:
        messages.error(request, f"La orden con código {codigo_oc} no existe.")
        return redirect("buscar_orden")

    return render(request, "despachos/consultar_orden.html", {"orden": orden})


def listar_despachos(request):
    pendientes = ProductoSolicitado.objects.filter(pendiente__gt=0)
    if pendientes.exists():
        messages.info(request, "Se muestran los productos pendientes por despacho.")
    else:
        messages.warning(request, "No hay productos pendientes por despachar.")
    return render(request, "despachos/listar_despachos.html", {"pendientes": pendientes})


def registrar_despacho(request, producto_id):
    producto_solicitado = get_object_or_404(ProductoSolicitado, id=producto_id)

    if request.method == "POST":
        form = DespachoForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data["cantidad"]

            # Validación: no se puede despachar más de lo pendiente
            if cantidad > producto_solicitado.pendiente:
                messages.error(
                    request,
                    f"No puedes despachar más de {producto_solicitado.pendiente} unidades."
                )
            else:
                # Crear el despacho
                despacho = form.save(commit=False)
                despacho.producto_solicitado = producto_solicitado
                despacho.save()

                # Se recalculan con las properties del modelo
                messages.success(
                    request,
                    f"Se registró el despacho de {cantidad} unidades."
                )
                return redirect(
                    "consultar_orden",
                    codigo_oc=producto_solicitado.orden.codigo_oc
                )
        else:
            messages.error(request, "El formulario contiene errores, revisa los campos.")
    else:
        form = DespachoForm()

    return render(
        request,
        "despachos/registrar_despacho.html",
        {"form": form, "producto": producto_solicitado}
    )
