from django.contrib import messages
from django.shortcuts import redirect, render

from taxis.decorators import rol_requerido
from taxis.forms.linea_form import LineaForm
from taxis.models import Linea, Usuario


@rol_requerido(Usuario.Rol.ADMIN)
def linea_list(request):
    """Listado de líneas de taxi."""
    contexto = {
        "titulo": "Líneas",
        "mensaje": "Las líneas agrupan los taxis por zona.",
        "lineas": Linea.objects.order_by("nombre"),
    }
    return render(request, "taxis/lineas/linea_list.html", contexto)


@rol_requerido(Usuario.Rol.ADMIN)
def linea_create(request):
    if request.method == "POST":
        form = LineaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Línea creada exitosamente.")
            return redirect("linea_list")
    else:
        form = LineaForm()
    return render(request, "taxis/lineas/linea_form.html", {
        "form": form,
        "encabezado": "Nueva línea",
    })
