from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .permisos import tiene_permiso

class SoloLecturaMixin(LoginRequiredMixin):
    """Mixin para vistas de solo lectura que solo permite ver"""
    permiso_requerido = None
    
    def dispatch(self, request, *args, **kwargs):
        if not tiene_permiso(request.user, self.permiso_requerido):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solo_lectura'] = True
        return context