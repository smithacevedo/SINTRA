from django import forms
from .models import Orden, DetalleOrden
from apps.clientes.models import Clientes
from apps.productos.models import Producto

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente']
        
class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['producto', 'cantidad']