from django import forms
from .models import Clientes

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre_cliente', 'email_cliente', 'nombre_contacto', 'telefono_contacto',
                  'email_contacto', 'direccion_cliente', 'ciudad_cliente', 'tiene_proyectos']