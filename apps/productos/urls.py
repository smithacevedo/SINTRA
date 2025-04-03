from django.urls import path
from .views import ListaProductosView, AgregarProductoView

urlpatterns = [
    path('lista_productos/', ListaProductosView.as_view(), name='lista_productos'),
    path('agregar_producto/', AgregarProductoView.as_view(), name='agregar_producto'),
]
