from django.db import models
from apps.permisos.models import Permiso


class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    permisos = models.ManyToManyField(Permiso, blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"