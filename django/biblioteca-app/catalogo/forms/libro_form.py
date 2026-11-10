from django import forms
from catalogo.models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 
                  'autor', 
                  'categoria', 
                  'fecha_publicacion', 
                  'isbn']
    widgets = {
        'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        'autor': forms.TextInput(attrs={'class': 'form-control'}),
        'categoria': forms.Select(attrs={'class': 'form-control'}),
        'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
        'isbn': forms.TextInput(attrs={'class': 'form-control'}),
    }