from django import forms
from .models import OrdenCompra, ProductoSolicitado
from django.forms import inlineformset_factory

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['codigo_oc', 'cliente', 'fecha_solicitud']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_solicitud': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'codigo_oc': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductoSolicitadoForm(forms.ModelForm):
    class Meta:
        model = ProductoSolicitado
        fields = ['producto', 'cantidad', 'descripcion']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formset para múltiples productos en una orden
ProductoFormSet = inlineformset_factory(
    OrdenCompra,
    ProductoSolicitado,
    form=ProductoSolicitadoForm,
    extra=1,
    can_delete=True
)
