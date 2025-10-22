from django.shortcuts import redirect
from django.urls import reverse
from .models import PerfilUsuario


class PrimerAccesoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            # Verificar si es primer acceso
            try:
                perfil = PerfilUsuario.objects.get(usuario=request.user)
                if perfil.primer_acceso:
                    # Permitir acceso solo a la página de cambio de contraseña y logout
                    allowed_paths = [
                        reverse('cambiar_password_obligatorio'),
                        reverse('logout'),
                        '/static/',  # Permitir archivos estáticos
                    ]
                    # Verificar si la ruta actual está permitida
                    path_allowed = any(request.path.startswith(path) for path in allowed_paths)
                    if not path_allowed:
                        return redirect('cambiar_password_obligatorio')
            except PerfilUsuario.DoesNotExist:
                # Si no existe perfil, crear uno marcando primer acceso
                PerfilUsuario.objects.create(usuario=request.user, primer_acceso=True)
                return redirect('cambiar_password_obligatorio')

        response = self.get_response(request)
        return response