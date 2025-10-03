from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.ordenes_compra.models import OrdenCompra, ProductoSolicitado
from .models import Despacho


def buscar_orden(request):
    if request.method == "POST":
        codigo_oc = request.POST.get("codigo_oc", "").strip()
        if codigo_oc:
            try:
                orden = OrdenCompra.objects.get(codigo_oc=codigo_oc)
                return redirect("despacho_unificado", codigo_oc=orden.codigo_oc)
            except OrdenCompra.DoesNotExist:
                messages.error(request, f"La orden {codigo_oc} no existe.")
    return render(request, "despachos/buscar_orden.html")


def despacho_unificado(request, codigo_oc):
    orden = get_object_or_404(OrdenCompra, codigo_oc=codigo_oc)
    
    if request.method == "POST":
        productos_seleccionados = request.POST.getlist('productos_seleccionados')
        despachos_realizados = 0
        
        for producto_id in productos_seleccionados:
            cantidad_str = request.POST.get(f'cantidad_{producto_id}')
            if cantidad_str:
                try:
                    cantidad = int(cantidad_str)
                    producto = get_object_or_404(ProductoSolicitado, id=producto_id)
                    
                    if cantidad > 0 and cantidad <= producto.pendiente:
                        Despacho.objects.create(
                            producto_solicitado=producto,
                            cantidad=cantidad
                        )
                        despachos_realizados += 1
                except (ValueError, TypeError):
                    continue
        
        if despachos_realizados > 0:
            messages.success(request, f"Se realizaron {despachos_realizados} despachos.")
    
    productos_pendientes = [p for p in orden.productos.all() if p.pendiente > 0]
    productos_despachados = [p for p in orden.productos.all() if p.despachado > 0]
    
    return render(request, 'despachos/despacho_unificado.html', {
        'orden': orden,
        'productos_pendientes': productos_pendientes,
        'productos_despachados': productos_despachados,
    })
