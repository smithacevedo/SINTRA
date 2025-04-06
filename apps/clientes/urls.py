from django.urls import path
from .views import ListaClientesView, AgregarClienteView, EditarClienteView, EliminarClienteView

urlpatterns = [
    path('lista_clientes/', ListaClientesView.as_view(), name='lista_clientes'),
    path('agregar_cliente/', AgregarClienteView.as_view(), name='agregar_cliente'),
    path('editar_cliente/<int:pk>/', EditarClienteView.as_view(), name='editar_cliente'),
    path('eliminar_cliente/<int:pk>/', EliminarClienteView.as_view(), name='eliminar_cliente'),
]