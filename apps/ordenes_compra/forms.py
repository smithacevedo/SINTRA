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

    def clean_codigo_oc(self):
        codigo_oc = self.cleaned_data.get('codigo_oc')
        if codigo_oc:
            qs = OrdenCompra.objects.filter(codigo_oc__iexact=codigo_oc)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Ya existe una orden de compra con este código.')
            return codigo_oc

class ProductoSolicitadoForm(forms.ModelForm):
    class Meta:
        model = ProductoSolicitado
        fields = ['producto', 'cantidad', 'descripcion']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control select2', 'required': True}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }

# Formset para múltiples productos en una orden
ProductoFormSet = inlineformset_factory(
    OrdenCompra,
    ProductoSolicitado,
    form=ProductoSolicitadoForm,
    extra=1,
    can_delete=True
)
