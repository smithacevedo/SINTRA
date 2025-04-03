from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy


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
