from django.db import models


class Permiso(models.Model):
    nombre = models.CharField(max_length=100)
    llave = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"