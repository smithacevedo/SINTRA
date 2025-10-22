from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from apps.clientes.forms import ClienteForm
from .models import Clientes
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.utils.permisos import requiere_permiso, tiene_permiso
from django.utils.decorators import method_decorator


class ListaClientesView(ListView):
    model = Clientes
    template_name = 'clientes/lista_clientes.html'
    context_object_name = 'clientes'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not tiene_permiso(request.user, 'ver_clientes'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'clientes'
        context['solo_lectura'] = not (tiene_permiso(self.request.user, 'crear_clientes') or 
                                      tiene_permiso(self.request.user, 'editar_clientes') or 
                                      tiene_permiso(self.request.user, 'eliminar_clientes'))
        return context

@method_decorator(requiere_permiso('crear_clientes'), name='dispatch')
class AgregarClienteView(LoginRequiredMixin, CreateView):
    model = Clientes
    form_class = ClienteForm
    template_name = 'clientes/agregar_cliente.html'
    success_url = reverse_lazy('lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'clientes'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El cliente ha sido agregado exitosamente.')
        return super().form_valid(form)


@method_decorator(requiere_permiso('editar_clientes'), name='dispatch')
class EditarClienteView(LoginRequiredMixin, UpdateView):
    model = Clientes
    form_class = ClienteForm
    template_name = 'clientes/editar_cliente.html'
    success_url = reverse_lazy('lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'clientes'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'El cliente "{form.instance.nombre_cliente}" ha sido actualizado exitosamente.')
        return response


@method_decorator(requiere_permiso('eliminar_clientes'), name='dispatch')
class EliminarClienteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        cliente.delete()
        messages.success(request, f'El cliente "{cliente.nombre_cliente}" ha sido eliminado.')
        return redirect('lista_clientes')