from django import forms

from taxis.models import Linea, TaxisFast


class TaxiForm(forms.ModelForm):
    """El chofer edita SU taxi: línea y datos. El estado se cambia con el botón del panel."""

    linea = forms.ModelChoiceField(
        queryset=Linea.objects.order_by("nombre"),
        label="Línea",
        required=False,
        empty_label="Sin línea",
        help_text="Elige la línea a la que perteneces. Si no ves la tuya, pídele al administrador que la cree.",
    )

    class Meta:
        model = TaxisFast
        fields = ["linea", "taxi", "taxi_placa", "taxi_tarifa"]
        labels = {
            "taxi": "Nombre del taxi",
            "taxi_placa": "Placa",
            "taxi_tarifa": "Tarifa",
        }
        widgets = {
            "taxi_placa": forms.TextInput(),
            "taxi_tarifa": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["taxi_placa"].required = True

    def clean_taxi_placa(self):
        placa = self.cleaned_data["taxi_placa"].strip().upper()
        otros = TaxisFast.objects.filter(taxi_placa__iexact=placa).exclude(pk=self.instance.pk)
        if otros.exists():
            raise forms.ValidationError("Ya hay un taxi registrado con esa placa.")
        return placa
