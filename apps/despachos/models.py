from django.db import models
from django.contrib.auth.models import User
from apps.ordenes_compra.models import ProductoSolicitado
from django.utils import timezone


class Despacho(models.Model):
    producto_solicitado = models.ForeignKey(
        ProductoSolicitado,
        on_delete=models.CASCADE,
        related_name="despachos"
    )
    fecha_despacho = models.DateTimeField(default=timezone.now)
    cantidad = models.PositiveIntegerField()
    reintegro = models.BooleanField(default=False)
    fecha_reintegro = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="despachos_creados",
        verbose_name="Creado por"
    )

    def save(self, *args, **kwargs):
        # Solo validar cantidad si es un nuevo despacho (no reintegro)
        if not self.pk and self.cantidad > self.producto_solicitado.pendiente:
            raise ValueError("No se puede despachar más de lo pendiente.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Despacho de {self.cantidad} - {self.producto_solicitado.producto.referencia}"
