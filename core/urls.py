# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include, re_path

from apps.home import views  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),             # UI Kits Html files
    path("productos/", include("apps.productos.urls")),
    path("clientes/", include("apps.clientes.urls")),
    path("ordenes_compra/", include("apps.ordenes_compra.urls")),
    path("proveedores/", include("apps.proveedores.urls")),
    path("despachos/", include('apps.despachos.urls')), 
    path("remisiones/", include('apps.remisiones.urls')),
    path("permisos/", include('apps.permisos.urls')),
    path("roles/", include('apps.roles.urls')),
    path("proyectos/", include("apps.proyectos.urls")),
   # path("detalles_orden/", include('apps.detalles_orden.urls')), 


    # Captura cualquier otro archivo HTML dentro de home (excluye las apps)
    #re_path(r'^(?!productos/|ventas/|clientes/).*\.html$', views.pages, name='pages'), CUANDO SEAN VARIOS
    re_path(r'^(?!productos/|clientes/).*\.html$', views.pages, name='pages'),
]
