from django.db import models
from cities_light.models import City
from apps.clientes.models import Clientes


class Proyectos(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='proyectos')
    nombre_proyecto = models.CharField(max_length=255)
    email_proyecto = models.EmailField(max_length=255, blank=True, null=True)
    nombre_contacto = models.CharField(max_length=255, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=10, blank=True, null=True)
    email_contacto = models.EmailField(max_length=255, blank=True, null=True)
    direccion_proyecto = models.CharField(max_length=255, blank=True, null=True)
    ciudad_proyecto = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nombre_proyecto + " - " + self.cliente.nombre_cliente
