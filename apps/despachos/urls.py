from django.urls import path
from . import views

urlpatterns = [
    path("", views.buscar_orden, name="buscar_orden"),
    path("<str:codigo_oc>/", views.despacho_unificado, name="despacho_unificado"),
    path("reintegrar/<int:despacho_id>/", views.reintegrar_despacho, name="reintegrar_despacho"),
]
