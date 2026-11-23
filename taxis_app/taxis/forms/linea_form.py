from django import forms

from taxis.models import Linea


class LineaForm(forms.ModelForm):
    class Meta:
        model = Linea
        fields = ["nombre", "zona", "zonas", "descripcion"]
        labels = {
            "zona": "Zona principal (texto)",
            "zonas": "Zonas que cubre",
        }
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
            "zonas": forms.CheckboxSelectMultiple(),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        repetidas = Linea.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk)
        if repetidas.exists():
            raise forms.ValidationError("Ya existe una línea con ese nombre.")
        return nombre
