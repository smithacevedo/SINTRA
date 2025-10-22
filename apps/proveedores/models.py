from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    productos_suministra = models.TextField(help_text="Lista de productos que suministra")

    def __str__(self):
        return self.nombre
