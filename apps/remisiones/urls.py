from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_remisiones, name='lista_remisiones'),
    path('<int:remision_id>/', views.detalle_remision, name='detalle_remision'),
    path('descargar/<int:remision_id>/', views.descargar_remision, name='descargar_remision'),
]