from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from apps.clientes.forms import ClienteForm
from .models import Clientes
from django.contrib import messages


class ListaClientesView(ListView):
    model = Clientes
    template_name = 'clientes/lista_clientes.html'
    context_object_name = 'clientes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'clientes'
        return context

class AgregarClienteView(CreateView):
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


class EditarClienteView(UpdateView):
    model = Clientes
    form_class = ClienteForm
    template_name = 'clientes/editar_cliente.html'
    success_url = reverse_lazy('lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'clientes'
        return context


class EliminarClienteView(View):
    def post(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        cliente.delete()
        messages.success(request, f'El cliente "{cliente.nombre_cliente}" ha sido eliminado.')
        return redirect('lista_clientes')