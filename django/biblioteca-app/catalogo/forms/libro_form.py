from django.utils import timezone

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

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if titulo:
            titulo = titulo.strip()
        if not titulo:
            raise forms.ValidationError("El título es obligatorio.")
        return titulo

    def clean_fecha_publicacion(self):
        fecha_publicacion = self.cleaned_data.get('fecha_publicacion')
        if fecha_publicacion and fecha_publicacion > timezone.localdate():
            raise forms.ValidationError("La fecha de publicación no puede ser futura.")
        if not fecha_publicacion:
            raise forms.ValidationError("La fecha de publicación es obligatoria.")
        return fecha_publicacion
    
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn:
            raise forms.ValidationError("El ISBN es obligatorio.")
        if len(isbn) != 13 or not isbn.isdigit():
            raise forms.ValidationError("El ISBN debe tener 13 dígitos numéricos.")
        return isbn