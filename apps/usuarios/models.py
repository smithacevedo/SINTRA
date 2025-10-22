from django.db import models
from django.contrib.auth.models import User
from apps.roles.models import Rol


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    primer_acceso = models.BooleanField(default=True, verbose_name='Primer Acceso')
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
    class Meta:
        db_table = 'perfil_usuario'
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'


class UsuarioRol(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles_usuario')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'usuario_rol'
        unique_together = ('usuario', 'rol')
        verbose_name = 'Usuario Rol'
        verbose_name_plural = 'Usuario Roles'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.rol.nombre}"