from django import forms

from taxis.models import Zona


class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ["nombre", "descripcion"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_nombre(self):
        return self.cleaned_data["nombre"].strip()
