from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from apps.usuarios.models import UsuarioRol

def requiere_permiso(clave_permiso):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Verificar si el usuario tiene el permiso
            if tiene_permiso(request.user, clave_permiso):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                return redirect('home')
        return wrapper
    return decorator

def tiene_permiso(usuario, clave_permiso):
    """Verifica si un usuario tiene un permiso específico"""
    try:
        roles_usuario = UsuarioRol.objects.filter(usuario=usuario)
        for usuario_rol in roles_usuario:
            if usuario_rol.rol.permisos.filter(clave=clave_permiso).exists():
                return True
        return False
    except:
        return False

def obtener_permisos_usuario(usuario):
    """Obtiene todos los permisos de un usuario"""
    permisos = set()
    try:
        roles_usuario = UsuarioRol.objects.filter(usuario=usuario)
        for usuario_rol in roles_usuario:
            for permiso in usuario_rol.rol.permisos.all():
                permisos.add(permiso.clave)
    except:
        pass
    return permisos