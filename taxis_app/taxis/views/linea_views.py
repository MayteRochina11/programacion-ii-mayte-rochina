from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from taxis.forms.linea_form import LineaForm
from taxis.models import Linea


@login_required
@permission_required("taxis.view_linea", raise_exception=True)
def linea_list(request):
    contexto = {
        "titulo": "Líneas",
        "mensaje": "Las líneas agrupan los taxis y cubren una o varias zonas.",
        "lineas": Linea.objects.prefetch_related("zonas").annotate(total_taxis=Count("taxis")),
    }
    return render(request, "taxis/lineas/linea_list.html", contexto)


@login_required
@permission_required("taxis.view_linea", raise_exception=True)
def linea_detail(request, pk):
    linea = get_object_or_404(Linea.objects.prefetch_related("zonas"), pk=pk)
    return render(request, "taxis/lineas/linea_detail.html", {
        "linea": linea,
        "taxis": linea.taxis.select_related("chofer"),
    })


@login_required
@permission_required("taxis.add_linea", raise_exception=True)
def linea_create(request):
    if request.method == "POST":
        form = LineaForm(request.POST)
        if form.is_valid():
            linea = form.save()
            messages.success(request, "Línea creada exitosamente.")
            return redirect(linea)
    else:
        form = LineaForm()
    return render(request, "taxis/lineas/linea_form.html", {
        "form": form,
        "encabezado": "Nueva línea",
    })


@login_required
@permission_required("taxis.change_linea", raise_exception=True)
def linea_update(request, pk):
    linea = get_object_or_404(Linea, pk=pk)
    if request.method == "POST":
        form = LineaForm(request.POST, instance=linea)
        if form.is_valid():
            form.save()
            messages.success(request, "Línea actualizada exitosamente.")
            return redirect(linea)
    else:
        form = LineaForm(instance=linea)
    return render(request, "taxis/lineas/linea_form.html", {
        "form": form,
        "encabezado": f"Editar línea: {linea.nombre}",
    })


@login_required
@permission_required("taxis.delete_linea", raise_exception=True)
def linea_delete(request, pk):
    linea = get_object_or_404(Linea, pk=pk)
    if request.method == "POST":
        linea.delete()
        messages.success(request, "Línea eliminada exitosamente.")
        return redirect("linea_list")
    return render(request, "taxis/lineas/linea_confirm_delete.html", {"linea": linea})
