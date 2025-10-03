from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
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
        
        errores = []
        despachos_creados = []
        
        for producto_id in productos_seleccionados:
            cantidad_str = request.POST.get(f'cantidad_{producto_id}')
            if cantidad_str:
                try:
                    cantidad = int(cantidad_str)
                    producto = get_object_or_404(ProductoSolicitado, id=producto_id)
                    
                    if cantidad <= 0:
                        errores.append(f"{producto.producto.referencia}: La cantidad debe ser mayor a 0")
                    elif cantidad > producto.pendiente:
                        errores.append(f"{producto.producto.referencia}: No puede despachar {cantidad}, solo hay {producto.pendiente} pendientes")
                    else:
                        despacho = Despacho.objects.create(
                            producto_solicitado=producto,
                            cantidad=cantidad
                        )
                        despachos_creados.append(despacho)
                        despachos_realizados += 1
                except (ValueError, TypeError):
                    errores.append(f"Producto {producto_id}: Cantidad inválida")
        
        if errores:
            for error in errores:
                messages.error(request, error)
        
        if despachos_realizados > 0:
            # Crear remisión automáticamente
            from apps.remisiones.models import Remision, DetalleRemision
            remision = Remision.objects.create(orden=orden)
            
            for despacho in despachos_creados:
                DetalleRemision.objects.create(
                    remision=remision,
                    despacho=despacho
                )
            
            messages.success(request, f"Se realizaron {despachos_realizados} despachos correctamente. Remisión: {remision.numero_remision}")
    
    productos_pendientes = [p for p in orden.productos.all() if p.pendiente > 0]
    productos_despachados = [p for p in orden.productos.all() if p.despachado > 0]
    
    return render(request, 'despachos/despacho_unificado.html', {
        'orden': orden,
        'productos_pendientes': productos_pendientes,
        'productos_despachados': productos_despachados,
    })


def reintegrar_despacho(request, despacho_id):
    despacho = get_object_or_404(Despacho, id=despacho_id)
    
    if not despacho.reintegro:
        despacho.reintegro = True
        despacho.fecha_reintegro = timezone.now()
        despacho.save()
        
        # Verificar si todos los despachos de la remisión están reintegrados
        if hasattr(despacho, 'remision_detalle'):
            remision = despacho.remision_detalle.remision
            despachos_activos = remision.detalles.filter(despacho__reintegro=False).count()
            
            if despachos_activos == 0:
                numero_remision = remision.numero_remision
                remision.delete()
                messages.success(request, f"Despacho reintegrado. Remisión {numero_remision} eliminada (todos los productos reintegrados).")
            else:
                messages.success(request, f"Despacho de {despacho.cantidad} unidades reintegrado.")
        else:
            messages.success(request, f"Despacho de {despacho.cantidad} unidades reintegrado.")
    else:
        messages.warning(request, "Este despacho ya fue reintegrado.")
    
    return redirect('despacho_unificado', codigo_oc=despacho.producto_solicitado.orden.codigo_oc)
