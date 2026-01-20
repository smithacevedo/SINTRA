from django import forms


class CargaMasivaForm(forms.Form):
    archivo = forms.FileField(
        label='Seleccionar archivo',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls,.csv',
            'id': 'archivo-cargue'
        })
    )
