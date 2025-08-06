from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Proveedor
from .forms import ProveedorForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages


class ListaproveedoresView(ListView):
    model = Proveedor
    template_name = 'proveedores/lista_proveedores.html'
    context_object_name = 'proveedores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'proveedores'  # Esta es una variable que se manda al template para identificar la sección actual
        return context


class AgregarproveedoresView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/agregar_proveedores.html'
    success_url = reverse_lazy('lista_proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'proveedores'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El proveedores ha sido agregado exitosamente.')
        return super().form_valid(form)


class EditarproveedoresView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/editar_proveedores.html'
    success_url = reverse_lazy('lista_proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'proveedores'
        return context


class EliminarproveedoresView(View):
    def post(self, request, pk, *args, **kwargs):
        proveedor = get_object_or_404(Proveedor, pk=pk)
        nombre_proveedor = proveedor.nombre 
        proveedor.delete()
        messages.success(request, f'El proveedor "{nombre_proveedor}" ha sido eliminado correctamente.')
        return redirect('lista_proveedores')
