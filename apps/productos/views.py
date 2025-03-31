from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


def lista_productos(request):
    productos = Producto.objects.all()
    context = {
        'productos': productos,
        'segment': 'productos'  # Esta es una variable que se manda al template para identificar la sección actual
    }
    return render(request, 'productos/lista_productos.html', context)


def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/agregar_producto.html', {'form': form})
