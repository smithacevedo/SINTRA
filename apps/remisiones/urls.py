from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_remisiones, name='lista_remisiones'),
    path('<int:remision_id>/', views.detalle_remision, name='detalle_remision'),
    path('descargar-excel/<int:remision_id>/', views.descargar_remision_excel, name='descargar_remision_excel'),
    path('descargar-pdf/<int:remision_id>/', views.descargar_remision_pdf, name='descargar_remision_pdf'),
    path('cambiar-estado/<int:remision_id>/', views.cambiar_estado_facturacion, name='cambiar_estado_facturacion'),
    path('subir-factura/<int:remision_id>/', views.subir_factura, name='subir_factura'),
    path('ver-factura/<int:remision_id>/', views.ver_factura, name='ver_factura'),
]