from django.db import models


class Clientes(models.Model):
    nombre_cliente = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_cliente