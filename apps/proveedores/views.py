from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Proveedor
from .forms import ProveedorForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.utils.permisos import requiere_permiso, tiene_permiso
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator


class ListaproveedoresView(ListView):
    model = Proveedor
    template_name = 'proveedores/lista_proveedores.html'
    context_object_name = 'proveedores'
    paginate_by = 15
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not tiene_permiso(request.user, 'ver_productos'):  # Proveedores usa permiso de productos
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'proveedores'
        context['solo_lectura'] = not (tiene_permiso(self.request.user, 'crear_productos') or 
                                      tiene_permiso(self.request.user, 'editar_productos') or 
                                      tiene_permiso(self.request.user, 'eliminar_productos'))
        return context


@method_decorator(requiere_permiso('crear_productos'), name='dispatch')
class AgregarproveedoresView(LoginRequiredMixin, CreateView):
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
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)


@method_decorator(requiere_permiso('editar_productos'), name='dispatch')
class EditarproveedoresView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/editar_proveedores.html'
    success_url = reverse_lazy('lista_proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'proveedores'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El proveedor ha sido actualizado exitosamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)


@method_decorator(requiere_permiso('eliminar_productos'), name='dispatch')
class EliminarproveedoresView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        proveedor = get_object_or_404(Proveedor, pk=pk)
        nombre_proveedor = proveedor.nombre 
        proveedor.delete()
        messages.success(request, f'El proveedor "{nombre_proveedor}" ha sido eliminado correctamente.')
        return redirect('lista_proveedores')
