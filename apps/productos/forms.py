from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['referencia', 'articulo', 'precio_costo', 'precio_venta', 'linea', 'descripcion']


    def clean_referencia(self):
        referencia = self.cleaned_data.get('referencia')
        if referencia:
            qs = Producto.objects.filter(referencia__iexact=referencia)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Ya existe un producto con esta referencia.')
        return referencia
