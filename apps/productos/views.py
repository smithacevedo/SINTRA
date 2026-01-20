from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Producto
from .forms import ProductoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.utils.permisos import requiere_permiso, tiene_permiso
from django.utils.decorators import method_decorator


class ListaProductosView(ListView):
    model = Producto
    template_name = 'productos/lista_productos.html'
    context_object_name = 'productos'
    paginate_by = 15
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not tiene_permiso(request.user, 'ver_productos'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'productos'
        # Solo lectura si solo tiene permiso de ver
        context['solo_lectura'] = not (tiene_permiso(self.request.user, 'crear_productos') or 
                                      tiene_permiso(self.request.user, 'editar_productos') or 
                                      tiene_permiso(self.request.user, 'eliminar_productos'))
        return context


@method_decorator(requiere_permiso('crear_productos'), name='dispatch')
class AgregarProductoView(LoginRequiredMixin, CreateView):
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


@method_decorator(requiere_permiso('editar_productos'), name='dispatch')
class EditarProductoView(LoginRequiredMixin, UpdateView):
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


@method_decorator(requiere_permiso('eliminar_productos'), name='dispatch')
class EliminarProductoView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        messages.success(request, f'El producto "{producto.referencia}" ha sido eliminado.')
        return redirect('lista_productos')
