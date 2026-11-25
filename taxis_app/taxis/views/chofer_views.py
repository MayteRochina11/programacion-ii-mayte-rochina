from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from taxis.forms.taxi_form import TaxiForm
from taxis.models import TaxisFast, Viaje


@login_required
@permission_required("taxis.aceptar_viaje", raise_exception=True)
def chofer_panel(request):
    if request.user.es_admin:
        return redirect("panel_admin")
    taxi = TaxisFast.objects.select_related("linea").filter(chofer=request.user).first()

    viaje_actual = None
    disponibles = Viaje.objects.none()
    historial = Viaje.objects.none()

    if taxi:
        viajes = Viaje.objects.select_related("creado_por")
        viaje_actual = viajes.filter(taxi=taxi, estado=Viaje.Estado.ASIGNADO).first()
        if taxi.estado == TaxisFast.Estado.EN_BASE:
            disponibles = viajes.filter(estado=Viaje.Estado.PENDIENTE).order_by("created_at")
        historial = viajes.filter(taxi=taxi, estado=Viaje.Estado.COMPLETADO)[:10]

    return render(request, "taxis/chofer/chofer_panel.html", {
        "titulo": "Panel del chofer",
        "taxi": taxi,
        "viaje_actual": viaje_actual,
        "disponibles": disponibles,
        "historial": historial,
    })


@login_required
@permission_required("taxis.change_taxisfast", raise_exception=True)
@require_POST
def chofer_disponibilidad(request):
    get_object_or_404(TaxisFast, chofer=request.user)
    with transaction.atomic():
        taxi = TaxisFast.objects.select_for_update().get(chofer=request.user)
        if taxi.estado == TaxisFast.Estado.EN_SERVICIO:
            messages.error(request, "Termina tu carrera en curso antes de cambiar tu disponibilidad.")
        elif taxi.estado == TaxisFast.Estado.EN_BASE:
            taxi.estado = TaxisFast.Estado.FUERA_DE_SERVICIO
            taxi.save(update_fields=["estado"])
            messages.success(request, "Estás fuera de servicio.")
        else:
            taxi.estado = TaxisFast.Estado.EN_BASE
            taxi.save(update_fields=["estado"])
            messages.success(request, "Estás disponible para recibir carreras.")
    return redirect("chofer_panel")


@login_required
@permission_required("taxis.change_taxisfast", raise_exception=True)
def chofer_taxi_edit(request):
    taxi = get_object_or_404(TaxisFast, chofer=request.user)
    if request.method == "POST":
        form = TaxiForm(request.POST, instance=taxi)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos de tu taxi actualizados.")
            return redirect("chofer_panel")
    else:
        form = TaxiForm(instance=taxi)
    return render(request, "taxis/chofer/chofer_taxi_form.html", {
        "form": form,
        "encabezado": "Mi taxi",
    })
