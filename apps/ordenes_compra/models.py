from django.db import models
from apps.clientes.models import Clientes
from django.utils import timezone
from apps.productos.models import Producto


class OrdenCompra(models.Model):
    codigo_oc = models.CharField(max_length=20, unique=True, blank=True, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='ordenes')
    fecha_solicitud = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Orden de {self.cliente.nombre_cliente} - {self.fecha_solicitud}"


class ProductoSolicitado(models.Model):
    orden = models.ForeignKey('OrdenCompra', on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.producto.referencia} - {self.cantidad}'
