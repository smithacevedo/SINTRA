from django.shortcuts import render, get_object_or_404
from .models import Remision, DetalleRemision


def lista_remisiones(request):
    buscar = request.GET.get('buscar', '')
    if buscar:
        remisiones = Remision.objects.filter(numero_remision__icontains=buscar).order_by('-fecha_remision')
    else:
        remisiones = Remision.objects.all().order_by('-fecha_remision')
    
    return render(request, 'remisiones/lista_remisiones.html', {
        'remisiones': remisiones,
        'buscar': buscar
    })


def detalle_remision(request, remision_id):
    remision = get_object_or_404(Remision, id=remision_id)
    detalles = remision.detalles.filter(despacho__reintegro=False)
    return render(request, 'remisiones/detalle_remision.html', {
        'remision': remision,
        'detalles': detalles
    })