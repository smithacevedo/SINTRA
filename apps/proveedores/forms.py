from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'nit', 'telefono', 'correo', 'direccion', 'productos_suministra']

    def clean_nit(self):
        nit = self.cleaned_data.get('nit')
        if nit and not nit.isdigit():
            raise forms.ValidationError("El NIT debe contener solo números.")
        
        qs = Proveedor.objects.filter(nit=nit)
        if self.instance.pk:  
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un proveedor registrado con este NIT.")

        return nit

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe ser solo números.")
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo and "@" not in correo or "." not in correo:
            raise forms.ValidationError("El correo debe contener un '@' y un '.'.")
        return correo
    
 
    
