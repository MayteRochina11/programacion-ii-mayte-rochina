# taxis/views.py
from django.shortcuts import redirect, render

from .forms import LineaForm, TaxiForm
from .models import Linea, TaxisFast


def taxi_lista(request):
    """Listado de la flota (página de inicio)."""
    contexto = {
        "titulo": "TaxisFast",
        "mensaje": "Tu taxi de confianza mas rapido del mercado",
        "taxis": TaxisFast.objects.select_related("linea").order_by("-taxi_fecha"),
        "total_en_base": TaxisFast.objects.filter(estado=TaxisFast.Estado.EN_BASE).count(),
        "total_en_servicio": TaxisFast.objects.filter(estado=TaxisFast.Estado.EN_SERVICIO).count(),
    }
    return render(request, "taxis/home.html", contexto)


def taxi_create(request):
    if request.method == "POST":
        form = TaxiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("taxis:home")
    else:
        form = TaxiForm()

    return render(request, "taxis/form.html", {
        "form": form,
        "encabezado": "Nuevo taxi",
        "url_cancelar": "taxis:home",
    })


def lineas_lista(request):
    """Listado de líneas de taxi."""
    contexto = {
        "titulo": "Líneas",
        "mensaje": "Las líneas agrupan los taxis por zona.",
        "lineas": Linea.objects.order_by("nombre"),
    }
    return render(request, "taxis/lineas.html", contexto)


def linea_create(request):
    if request.method == "POST":
        form = LineaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("taxis:lineas_lista")
    else:
        form = LineaForm()

    return render(request, "taxis/form.html", {
        "form": form,
        "encabezado": "Nueva línea",
        "url_cancelar": "taxis:lineas_lista",
    })


def sobre_nosotros(request):
    contexto = {
        "titulo": "Sobre TaxisFast",
        "mensaje": "Conoce un poco más sobre nuestra misión y visión.",
    }
    return render(request, "taxis/sobre_nosotros.html", contexto)
