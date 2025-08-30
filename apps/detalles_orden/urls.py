from django.urls import path
from .views import CrearOrdenView, DetalleOrdenView, ListarPendientesView, MarcarDespachadoView

urlpatterns = [
    path('orden/nueva/', CrearOrdenView.as_view(), name='crear_orden'),
    path('orden/<int:orden_id>/', DetalleOrdenView.as_view(), name='detalle_orden'),
    path('despachos/pendientes/', ListarPendientesView.as_view(), name='listar_pendientes'),
    path('despachos/marcar/<int:detalle_id>/', MarcarDespachadoView.as_view(), name='marcar_despachado'),
]
