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

    # Captura cualquier otro archivo HTML dentro de home (excluye las apps)
    #re_path(r'^(?!productos/|ventas/|clientes/).*\.html$', views.pages, name='pages'), CUANDO SEAN VARIOS
    re_path(r'^(?!productos/|clientes/).*\.html$', views.pages, name='pages'),
]
