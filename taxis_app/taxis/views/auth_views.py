from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from taxis.forms.registro_form import LoginForm, RegistroChoferForm, RegistroPasajeroForm


def ingresar(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        siguiente = request.GET.get("next", "")
        if url_has_allowed_host_and_scheme(
            siguiente, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        ):
            return redirect(siguiente)
        return redirect("inicio")

    return render(request, "taxis/auth/login.html", {"form": form})


@require_POST
def salir(request):
    logout(request)
    messages.success(request, "Cerraste sesión.")
    return redirect("inicio")


def _registro(request, form_class, encabezado, subtitulo):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "¡Cuenta creada! Bienvenido a TaxisFast.")
            return redirect("inicio")
    else:
        form = form_class()

    return render(request, "taxis/auth/registro.html", {
        "form": form,
        "encabezado": encabezado,
        "subtitulo": subtitulo,
    })


def registro_pasajero(request):
    return _registro(
        request, RegistroPasajeroForm,
        "Registro de pasajero", "Crea tu cuenta para pedir carreras.",
    )


def registro_chofer(request):
    return _registro(
        request, RegistroChoferForm,
        "Registro de chofer", "Crea tu cuenta y registra tu taxi para recibir carreras.",
    )
