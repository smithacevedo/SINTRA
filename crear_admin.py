#!/usr/bin/env python
"""
Script para crear usuario administrador con acceso completo
Ejecutar con: python crear_admin.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from apps.roles.models import Rol
from apps.usuarios.models import UsuarioRol, PerfilUsuario

def crear_usuario_admin():
    # Crear usuario
    usuario, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'email': 'admin@sintra.com',
            'is_staff': True,
            'is_active': True,
            'is_superuser': True
        }
    )
    
    if created:
        usuario.set_password('admin123')
        usuario.save()
        print(f"Usuario '{usuario.username}' creado exitosamente")
    else:
        print(f"Usuario '{usuario.username}' ya existe")
    
    # Crear perfil
    perfil, created = PerfilUsuario.objects.get_or_create(
        usuario=usuario,
        defaults={'primer_acceso': False}
    )
    
    if created:
        print("Perfil de usuario creado")
    
    # Asignar rol Administrador
    try:
        rol_admin = Rol.objects.get(nombre='Administrador')
        usuario_rol, created = UsuarioRol.objects.get_or_create(
            usuario=usuario,
            rol=rol_admin
        )
        
        if created:
            print("Rol Administrador asignado")
        else:
            print("Rol Administrador ya estaba asignado")
            
    except Rol.DoesNotExist:
        print("ERROR: Rol 'Administrador' no existe. Ejecuta primero el script SQL.")
        return
    
    print("\n=== USUARIO ADMINISTRADOR ===")
    print(f"Usuario: {usuario.username}")
    print(f"Contraseña: admin123")
    print(f"Email: {usuario.email}")
    print("Acceso: COMPLETO")

if __name__ == '__main__':
    crear_usuario_admin()