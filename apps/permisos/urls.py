from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_permisos, name='lista_permisos'),
    path('crear/', views.crear_permiso, name='crear_permiso'),
    path('editar/<int:permiso_id>/', views.editar_permiso, name='editar_permiso'),
    path('eliminar/<int:permiso_id>/', views.eliminar_permiso, name='eliminar_permiso'),
]