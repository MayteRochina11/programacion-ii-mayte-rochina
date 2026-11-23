from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from taxis.decorators import rol_requerido
from taxis.forms.zona_form import ZonaForm
from taxis.models import TaxisFast, Usuario, Zona


@login_required
def zona_list(request):
    contexto = {
        "titulo": "Zonas",
        "mensaje": "Sectores de la ciudad que cubren las líneas.",
        "zonas": Zona.objects.annotate(total_lineas=Count("lineas")),
    }
    return render(request, "taxis/zonas/zona_list.html", contexto)


@login_required
def zona_detail(request, pk):
    zona = get_object_or_404(Zona, pk=pk)
    return render(request, "taxis/zonas/zona_detail.html", {
        "zona": zona,
        "lineas": zona.lineas.all(),
        # Los taxis que operan en la zona son los de las líneas que la cubren.
        "taxis": TaxisFast.objects.filter(linea__zonas=zona).select_related("chofer", "linea").distinct(),
    })


@login_required
@rol_requerido(Usuario.Rol.ADMIN)
def zona_create(request):
    if request.method == "POST":
        form = ZonaForm(request.POST)
        if form.is_valid():
            zona = form.save()
            messages.success(request, "Zona creada exitosamente.")
            return redirect(zona)
    else:
        form = ZonaForm()
    return render(request, "taxis/zonas/zona_form.html", {
        "form": form,
        "encabezado": "Nueva zona",
    })


@login_required
@rol_requerido(Usuario.Rol.ADMIN)
def zona_update(request, pk):
    zona = get_object_or_404(Zona, pk=pk)
    if request.method == "POST":
        form = ZonaForm(request.POST, instance=zona)
        if form.is_valid():
            form.save()
            messages.success(request, "Zona actualizada exitosamente.")
            return redirect(zona)
    else:
        form = ZonaForm(instance=zona)
    return render(request, "taxis/zonas/zona_form.html", {
        "form": form,
        "encabezado": f"Editar zona: {zona.nombre}",
    })


@login_required
@rol_requerido(Usuario.Rol.ADMIN)
def zona_delete(request, pk):
    """GET muestra la confirmación; solo POST elimina."""
    zona = get_object_or_404(Zona, pk=pk)
    if request.method == "POST":
        zona.delete()
        messages.success(request, "Zona eliminada exitosamente.")
        return redirect("zona_list")
    return render(request, "taxis/zonas/zona_confirm_delete.html", {"zona": zona})
