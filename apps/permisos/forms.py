from django import forms
from .models import Permiso


class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['nombre', 'llave']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'llave': forms.TextInput(attrs={'class': 'form-control'}),
        }