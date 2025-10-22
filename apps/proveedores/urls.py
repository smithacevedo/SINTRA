from django.urls import path
from .views import ListaproveedoresView, AgregarproveedoresView, EditarproveedoresView, EliminarproveedoresView

urlpatterns = [
    path('lista-proveedores/', ListaproveedoresView.as_view(), name='lista_proveedores'),
    path('agregar-proveedores/', AgregarproveedoresView.as_view(), name='agregar_proveedores'),
    path('editar-proveedores/<int:pk>/', EditarproveedoresView.as_view(), name='editar_proveedores'),
    path('eliminar-proveedores/<int:pk>/', EliminarproveedoresView.as_view(), name='eliminar_proveedores'),
]
