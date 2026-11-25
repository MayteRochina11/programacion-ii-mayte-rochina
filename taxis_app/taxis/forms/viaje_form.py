from django import forms

from taxis.models import Viaje


class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ["origen", "destino"]
        widgets = {
            "origen": forms.TextInput(attrs={"placeholder": "¿Dónde te recogemos?"}),
            "destino": forms.TextInput(attrs={"placeholder": "¿A dónde vas?"}),
        }

    def clean(self):
        datos = super().clean()
        origen, destino = datos.get("origen"), datos.get("destino")
        if origen and destino and origen.strip().lower() == destino.strip().lower():
            raise forms.ValidationError("El origen y el destino no pueden ser el mismo lugar.")
        return datos
