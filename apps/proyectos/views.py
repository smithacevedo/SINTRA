from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from apps.proyectos.forms import ProyectoForm
from apps.proyectos.models import Proyectos
from apps.utils.permisos import requiere_permiso, tiene_permiso
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator


class ListaProyectosView(ListView):
    model = Proyectos
    template_name = 'proyectos/lista_proyectos.html'
    context_object_name = 'proyectos'
    paginate_by = 15
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not tiene_permiso(request.user, 'ver_productos'):  # Proyectos usa permiso de productos
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'proyectos'
        context['solo_lectura'] = not (tiene_permiso(self.request.user, 'crear_productos') or 
                                      tiene_permiso(self.request.user, 'editar_productos') or 
                                      tiene_permiso(self.request.user, 'eliminar_productos'))
        return context

@method_decorator(requiere_permiso('crear_productos'), name='dispatch')
class AgregarProyectoView(LoginRequiredMixin, CreateView):
    model = Proyectos
    form_class = ProyectoForm
    template_name = 'proyectos/agregar_proyecto.html'
    success_url = reverse_lazy('lista_proyectos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'proyectos'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El proyecto ha sido agregado exitosamente.')
        return super().form_valid(form)


@method_decorator(requiere_permiso('editar_productos'), name='dispatch')
class EditarProyectoView(LoginRequiredMixin, UpdateView):
    model = Proyectos
    form_class = ProyectoForm
    template_name = 'proyectos/editar_proyecto.html'
    success_url = reverse_lazy('lista_proyectos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'proyectos'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'El proyecto "{form.instance.nombre_proyecto}" ha sido actualizado exitosamente.')
        return response


@method_decorator(requiere_permiso('eliminar_productos'), name='dispatch')
class EliminarProyectoView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        proyecto = get_object_or_404(Proyectos, pk=pk)
        proyecto.delete()
        messages.success(request, f'El proyecto "{proyecto.nombre_proyecto}" ha sido eliminado.')
        return redirect('lista_proyectos')
