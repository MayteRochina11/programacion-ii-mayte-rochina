from django import forms

from taxis.models import Linea


class LineaForm(forms.ModelForm):
    class Meta:
        model = Linea
        fields = ["nombre", "zona", "descripcion"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }
