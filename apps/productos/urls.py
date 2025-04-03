from django.urls import path
from .views import ListaProductosView, AgregarProductoView, EditarProductoView, EliminarProductoView

urlpatterns = [
    path('lista_productos/', ListaProductosView.as_view(), name='lista_productos'),
    path('agregar_producto/', AgregarProductoView.as_view(), name='agregar_producto'),
    path('editar_producto/<int:pk>/', EditarProductoView.as_view(), name='editar_producto'),
    path('eliminar_producto/<int:pk>/', EliminarProductoView.as_view(), name='eliminar_producto'),
]
