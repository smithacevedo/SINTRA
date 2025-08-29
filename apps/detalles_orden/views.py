from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Orden, DetalleOrden
from .forms import OrdenForm, DetalleOrdenForm


class CrearOrdenView(CreateView):
    """
    Crear una nueva orden de despacho.
    """
    model = Orden
    form_class = OrdenForm
    template_name = 'detalles_orden/crear_orden.html'

    def form_valid(self, form):
        orden = form.save()
        messages.success(self.request, "Orden creada exitosamente.")
        return redirect('detalle_orden', orden_id=orden.id)

    def form_invalid(self, form):
        messages.error(self.request, "Corrige los errores en el formulario.")
        return super().form_invalid(form)


class DetalleOrdenView(DetailView):
    """
    Muestra los detalles de una orden y permite agregar productos.
    """
    model = Orden
    template_name = 'detalles_orden/detalle_orden.html'
    pk_url_kwarg = 'orden_id'
    context_object_name = 'orden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DetalleOrdenForm()
        context['detalles'] = DetalleOrden.objects.filter(orden=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = DetalleOrdenForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.orden = self.object
            detalle.save()
            messages.success(request, "Producto agregado a la orden.")
            return redirect('detalle_orden', orden_id=self.object.id)
        else:
            messages.error(request, "Hubo un error al agregar el producto.")
        return self.render_to_response(self.get_context_data(form=form))


class ListarPendientesView(ListView):
    """
    Lista todos los productos pendientes de despacho.
    """
    model = DetalleOrden
    template_name = 'detalles_orden/listar_pendientes.html'
    context_object_name = 'pendientes'

    def get_queryset(self):
        return DetalleOrden.objects.filter(despachado=False).order_by('orden__fecha_creacion')


class MarcarDespachadoView(View):
    """
    Marca un producto específico como despachado.
    """
    def post(self, request, detalle_id, *args, **kwargs):
        detalle = get_object_or_404(DetalleOrden, pk=detalle_id)
        detalle.despachado = True
        detalle.save()

        # Si todos los detalles de la orden están despachados, marca la orden como completada
        if not DetalleOrden.objects.filter(orden=detalle.orden, despachado=False).exists():
            orden = detalle.orden
            orden.completada = True
            orden.save()

        messages.success(request, f'Producto "{detalle.producto}" marcado como despachado.')
        return HttpResponseRedirect(reverse('listar_pendientes'))
