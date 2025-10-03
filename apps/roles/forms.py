from django import forms
from .models import Rol
from apps.permisos.models import Permiso


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'permisos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'permisos': forms.CheckboxSelectMultiple(),
        }