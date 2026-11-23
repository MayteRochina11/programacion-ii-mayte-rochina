from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from taxis.decorators import rol_requerido
from taxis.forms.taxi_form import TaxiForm
from taxis.models import TaxisFast, Usuario, Viaje


@login_required
@rol_requerido(Usuario.Rol.CHOFER)
def chofer_panel(request):
    """Panel del chofer: su taxi, su carrera en curso y las carreras que puede aceptar."""
    taxi = TaxisFast.objects.select_related("linea").filter(chofer=request.user).first()

    viaje_actual = None
    disponibles = Viaje.objects.none()
    historial = Viaje.objects.none()

    if taxi:
        viajes = Viaje.objects.select_related("pasajero")
        viaje_actual = viajes.filter(taxi=taxi, estado=Viaje.Estado.ASIGNADO).first()
        if taxi.estado == TaxisFast.Estado.EN_BASE:
            # Las más antiguas primero: llevan más tiempo esperando.
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
@rol_requerido(Usuario.Rol.CHOFER)
@require_POST
def chofer_disponibilidad(request):
    """Alterna entre 'En la base' (disponible) y 'Fuera de servicio'."""
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
@rol_requerido(Usuario.Rol.CHOFER)
def chofer_taxi_edit(request):
    """El chofer cambia su línea y los datos de SU taxi (nunca el de otro)."""
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
