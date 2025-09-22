from django.urls import path
from . import views

urlpatterns = [
    path("buscar-orden/", views.buscar_orden, name="buscar_orden"),
    path("orden/<str:codigo_oc>/", views.consultar_orden, name="consultar_orden"),
    path("despacho/<int:producto_id>/", views.registrar_despacho, name="registrar_despacho"),
    path("pendientes/", views.listar_despachos, name="listar_despachos"),
]
