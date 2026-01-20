from django.urls import path
from . import views

app_name = 'cargues_masivos'

urlpatterns = [
    path('', views.lista_cargues, name='lista_cargues'),
    path('cargue/<str:tipo_cargue>/', views.cargue_detalle, name='cargue_detalle'),
]
