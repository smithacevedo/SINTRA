from django import forms
from apps.clientes.models import Clientes
from .models import Proyectos

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.filter(tiene_proyectos=True)