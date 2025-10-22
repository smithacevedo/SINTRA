# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Sum, Count, Q
from apps.productos.models import Producto
from apps.clientes.models import Clientes
from apps.proyectos.models import Proyectos
from apps.ordenes_compra.models import OrdenCompra, ProductoSolicitado
from apps.proveedores.models import Proveedor
from apps.despachos.models import Despacho
from apps.remisiones.models import Remision


@login_required(login_url="/login/")
def index(request):
    # Métricas generales
    total_productos = Producto.objects.count()
    total_clientes = Clientes.objects.count()
    total_proyectos = Proyectos.objects.count()
    total_proveedores = Proveedor.objects.count()
    
    # Métricas de órdenes
    total_ordenes = OrdenCompra.objects.count()
    
    # Órdenes con productos pendientes
    ordenes_con_pendientes = OrdenCompra.objects.filter(
        productos__cantidad__gt=0
    ).distinct().select_related('cliente')[:10]
    ordenes_pendientes_count = OrdenCompra.objects.filter(
        productos__cantidad__gt=0
    ).distinct().count()
    
    # Métricas de despachos
    total_despachos = Despacho.objects.filter(reintegro=False).count()
    total_reintegros = Despacho.objects.filter(reintegro=True).count()
    
    # Métricas de remisiones
    total_remisiones = Remision.objects.count()
    
    # Órdenes recientes
    ordenes_recientes = OrdenCompra.objects.select_related('cliente').order_by('-fecha_solicitud')[:5]
    
    # Remisiones recientes
    remisiones_recientes = Remision.objects.select_related('orden__cliente').order_by('-fecha_remision')[:5]
    
    context = {
        'segment': 'index',
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_proyectos': total_proyectos,
        'total_proveedores': total_proveedores,
        'total_ordenes': total_ordenes,
        'ordenes_pendientes_count': ordenes_pendientes_count,
        'ordenes_pendientes': ordenes_con_pendientes,
        'total_despachos': total_despachos,
        'total_reintegros': total_reintegros,
        'total_remisiones': total_remisiones,
        'ordenes_recientes': ordenes_recientes,
        'remisiones_recientes': remisiones_recientes,
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
