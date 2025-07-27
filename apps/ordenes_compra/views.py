from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages

from .models import OrdenCompra, ProductoSolicitado
from .forms import OrdenCompraForm, ProductoFormSet


class ListaOrdenesCompraView(ListView):
    model = OrdenCompra
    template_name = 'ordenes_compra/lista_ordenes_compra.html'
    context_object_name = 'ordenes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'ordenes'
        return context


class AgregarOrdenCompraView(CreateView):
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'ordenes_compra/agregar_orden_compra.html'
    success_url = reverse_lazy('lista_ordenes_compra')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = ProductoFormSet(prefix='productosolicitado_set')
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'segment': 'ordenes'
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = ProductoFormSet(request.POST, prefix='productosolicitado_set')

        if form.is_valid() and formset.is_valid():
            orden = form.save()
            productos = formset.save(commit=False)
            for p in productos:
                p.orden = orden
                p.save()
            messages.success(request, 'La orden de compra ha sido registrada exitosamente.')
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'segment': 'ordenes'
        })


class EditarOrdenCompraView(UpdateView):
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'ordenes_compra/editar_orden_compra.html'
    success_url = reverse_lazy('lista_ordenes_compra')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProductoFormSet(
                self.request.POST, 
                instance=self.object, 
                prefix='productosolicitado_set'
            )
        else:
            context['formset'] = ProductoFormSet(
                instance=self.object, 
                prefix='productosolicitado_set'
            )
        context['segment'] = 'ordenes'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'La orden de compra ha sido actualizada correctamente.')
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form))


class EliminarOrdenCompraView(View):
    def post(self, request, pk, *args, **kwargs):
        orden = get_object_or_404(OrdenCompra, pk=pk)
        orden.delete()
        messages.success(request, f'La orden de compra del cliente "{orden.cliente.nombre_cliente}" ha sido eliminada.')
        return redirect('lista_ordenes_compra')
