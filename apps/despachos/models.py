from django.db import models
from apps.ordenes_compra.models import ProductoSolicitado


class Despacho(models.Model):
    producto_solicitado = models.ForeignKey(
        ProductoSolicitado,
        on_delete=models.CASCADE,
        related_name="despachos"
    )
    fecha_despacho = models.DateField(auto_now_add=True)
    cantidad = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.cantidad > self.producto_solicitado.pendiente:
            raise ValueError("No se puede despachar más de lo pendiente.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Despacho de {self.cantidad} - {self.producto_solicitado.producto.referencia}"
