from django.db import models
from django.core.exceptions import ValidationError

from apps.proveedores.models import Proveedor

class Producto(models.Model):

    LINEA_CHOICES = [
        ('HOMBRE', 'Hombre'),
        ('DAMA', 'Dama'),
        ('UNISEX', 'Unisex'),
    ]

    referencia = models.CharField(max_length=50, unique=True)
    articulo = models.CharField(max_length=100, blank=True, null=True)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    linea = models.CharField(max_length=50, choices=LINEA_CHOICES, blank=True, null=True)
    descripcion = models.TextField()
    referencia_externa = models.BooleanField(default=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')

    def __str__(self):
        return self.referencia

    def clean(self):
        """Validación a nivel de modelo: si es referencia externa, requiere proveedor."""
        if self.referencia_externa and not self.proveedor:
            raise ValidationError({'proveedor': 'Para productos marcados como referencia externa, el proveedor es obligatorio.'})
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
