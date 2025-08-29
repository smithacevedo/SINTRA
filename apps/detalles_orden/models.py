from django.db import models
from apps.clientes.models import Clientes
from apps.productos.models import Producto


class Orden(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_despacho = models.DateTimeField(null=True, blank=True)
    completada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Orden #{self.id} de {self.cliente.nombre}"

class DetalleOrden(models.Model):

    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    despachado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('orden', 'producto')

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} en Orden #{self.orden.id}"