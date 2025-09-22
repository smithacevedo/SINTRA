from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from apps.proyectos.forms import ProyectoForm
from apps.proyectos.models import Proyectos


class ListaProyectosView(ListView):
    model = Proyectos
    template_name = 'proyectos/lista_proyectos.html'
    context_object_name = 'proyectos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'proyectos'
        return context

class AgregarProyectoView(CreateView):
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


class EditarProyectoView(UpdateView):
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


class EliminarProyectoView(View):
    def post(self, request, pk, *args, **kwargs):
        proyecto = get_object_or_404(Proyectos, pk=pk)
        proyecto.delete()
        messages.success(request, f'El proyecto "{proyecto.nombre_proyecto}" ha sido eliminado.')
        return redirect('lista_proyectos')
