from django.urls import path
from .views import ListaProyectosView, AgregarProyectoView, EditarProyectoView, EliminarProyectoView

urlpatterns = [
    path('lista_proyectos/', ListaProyectosView.as_view(), name='lista_proyectos'),
    path('agregar_proyecto/', AgregarProyectoView.as_view(), name='agregar_proyecto'),
    path('editar_proyecto/<int:pk>/', EditarProyectoView.as_view(), name='editar_proyecto'),
    path('eliminar_proyecto/<int:pk>/', EliminarProyectoView.as_view(), name='eliminar_proyecto'),
]