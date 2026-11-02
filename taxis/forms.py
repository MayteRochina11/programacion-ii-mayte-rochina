# taxis/forms.py
from django import forms

from .models import Linea, TaxisFast


class LineaForm(forms.ModelForm):
    class Meta:
        model = Linea
        fields = ["nombre", "zona", "descripcion"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }


class TaxiForm(forms.ModelForm):
    class Meta:
        model = TaxisFast
        fields = ["linea", "taxi", "taxi_placa", "taxi_chofer", "taxi_tarifa", "estado"]
        widgets = {
            "taxi_placa": forms.TextInput(),
            "taxi_chofer": forms.TextInput(),
            "taxi_tarifa": forms.TextInput(),
        }
