from django import forms
from .models import Proyectos

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = '__all__'