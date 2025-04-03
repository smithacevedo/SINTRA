from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['referencia', 'articulo', 'precio_costo', 'precio_venta', 'linea', 'descripcion']
