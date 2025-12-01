from django.urls import path
from .views import AgregarOrdenCompraView, ListaOrdenesCompraView, EditarOrdenCompraView, EliminarOrdenCompraView, remisiones_orden

urlpatterns = [
    path('agregar-orden-compra/', AgregarOrdenCompraView.as_view(), name='agregar_orden_compra'),
    path('lista-ordenes-compra/', ListaOrdenesCompraView.as_view(), name='lista_ordenes_compra'),
    path('editar-orden-compra/<int:pk>/', EditarOrdenCompraView.as_view(), name='editar_orden_compra'),
    path('eliminar-orden-compra/<int:pk>/', EliminarOrdenCompraView.as_view(), name='eliminar_orden_compra'),
    path('remisiones/<int:pk>/', remisiones_orden, name='remisiones_orden'),
]
