from django import forms
from .models import Despacho

class DespachoForm(forms.ModelForm):
    class Meta:
        model = Despacho
        fields = ["cantidad"]  # Solo pedimos la cantidad a despachar
