from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction

from taxis.models import Linea, TaxisFast, Usuario


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_login": "Usuario o contraseña incorrectos.",
        "inactive": "Esta cuenta está desactivada.",
    }


class RegistroBaseForm(UserCreationForm):
    """UserCreationForm extendido: pide también nombre, correo y teléfono.

    El ROL lo fija cada subclase, nunca viene del formulario.
    """

    rol = None

    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "telefono")
        labels = {
            "username": "Usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
            "telefono": "Teléfono",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in ("first_name", "last_name", "email", "telefono"):
            self.fields[campo].required = True

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese correo.")
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol = self.rol
        if commit:
            usuario.save()
        return usuario


class RegistroPasajeroForm(RegistroBaseForm):
    rol = Usuario.Rol.PASAJERO


class RegistroChoferForm(RegistroBaseForm):
    """Registra al chofer Y su taxi en un solo paso."""

    rol = Usuario.Rol.CHOFER

    taxi = forms.CharField(max_length=100, label="Nombre del taxi")
    taxi_placa = forms.CharField(max_length=20, label="Placa")
    taxi_tarifa = forms.DecimalField(
        label="Tarifa",
        required=False,
        max_digits=6,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
    )
    linea = forms.ModelChoiceField(
        queryset=Linea.objects.order_by("nombre"),
        label="Línea",
        required=False,
        empty_label="Sin línea por ahora",
        help_text="Podrás cambiarla después desde tu panel.",
    )

    field_order = [
        "username", "first_name", "last_name", "email", "telefono",
        "password1", "password2",
        "taxi", "taxi_placa", "taxi_tarifa", "linea",
    ]

    def clean_taxi_placa(self):
        placa = self.cleaned_data["taxi_placa"].strip().upper()
        if TaxisFast.objects.filter(taxi_placa__iexact=placa).exists():
            raise forms.ValidationError("Ya hay un taxi registrado con esa placa.")
        return placa

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if commit:
            with transaction.atomic():
                usuario.save()
                TaxisFast.objects.create(
                    chofer=usuario,
                    linea=self.cleaned_data["linea"],
                    taxi=self.cleaned_data["taxi"],
                    taxi_placa=self.cleaned_data["taxi_placa"],
                    taxi_tarifa=self.cleaned_data["taxi_tarifa"],
                )
        return usuario
