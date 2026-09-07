from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['referencia', 'articulo', 'precio_costo', 'precio_venta', 'linea', 'descripcion', 'referencia_externa', 'proveedor']

    def clean_referencia(self):
        referencia = self.cleaned_data.get('referencia')
        if referencia:
            qs = Producto.objects.filter(referencia__iexact=referencia)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Ya existe un producto con esta referencia.')
        return referencia

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir clases CSS para integrarse con Select2 y estilos existentes
        if 'proveedor' in self.fields:
            self.fields['proveedor'].widget.attrs.update({'class': 'form-control select2'})
        if 'linea' in self.fields:
            self.fields['linea'].widget.attrs.update({'class': 'form-control select2'})
        if 'referencia_externa' in self.fields:
            self.fields['referencia_externa'].widget.attrs.update({'class': 'form-check-input'})
