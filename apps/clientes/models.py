from django.db import models
from cities_light.models import City


class Clientes(models.Model):
    nombre_cliente = models.CharField(max_length=255)
    email_cliente = models.EmailField(max_length=255, blank=True, null=True)
    nombre_contacto = models.CharField(max_length=255, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=10, blank=True, null=True)
    email_contacto = models.EmailField(max_length=255, blank=True, null=True)
    direccion_cliente = models.CharField(max_length=255, blank=True, null=True)
    ciudad_cliente = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    tiene_proyectos = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_cliente