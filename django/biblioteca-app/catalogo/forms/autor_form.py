from django import forms
from catalogo.models import Autor
from django.core.exceptions import ValidationError

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 
                  'apellido', 
                  'nacionalidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
        }
