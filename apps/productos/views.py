from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Producto
from .forms import ProductoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages


class ListaProductosView(ListView):
    model = Producto
    template_name = 'productos/lista_productos.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'productos'  # Esta es una variable que se manda al template para identificar la sección actual
        return context


class AgregarProductoView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/agregar_producto.html'
    success_url = reverse_lazy('lista_productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'productos'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El producto ha sido agregado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)


class EditarProductoView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/editar_producto.html'
    success_url = reverse_lazy('lista_productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'productos'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El producto ha sido actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)


class EliminarProductoView(View):
    def post(self, request, pk, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        messages.success(request, f'El producto "{producto.referencia}" ha sido eliminado.')
        return redirect('lista_productos')
