from django import forms

from taxis.models import Viaje


class ViajeForm(forms.ModelForm):
    """El pasajero solo escribe origen y destino; el pasajero se toma de su sesión."""

    class Meta:
        model = Viaje
        fields = ["origen", "destino"]
