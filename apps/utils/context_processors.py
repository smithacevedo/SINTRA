from .permisos import obtener_permisos_usuario

def permisos_usuario(request):
    """Context processor para hacer disponibles los permisos del usuario en todos los templates"""
    if request.user.is_authenticated:
        return {
            'permisos_usuario': obtener_permisos_usuario(request.user)
        }
    return {
        'permisos_usuario': set()
    }