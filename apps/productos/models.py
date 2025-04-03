from django.db import models

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

    def __str__(self):
        return self.referencia
