from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from taxis.decorators import rol_requerido
from taxis.forms.viaje_form import ViajeForm
from taxis.models import TaxisFast, Usuario, Viaje


@rol_requerido(Usuario.Rol.PASAJERO)
def viaje_list(request):
    """El pasajero ve SOLO sus propias carreras."""
    contexto = {
        "titulo": "Mis viajes",
        "mensaje": "Pide una carrera y un chofer la aceptará.",
        "viajes": Viaje.objects.filter(pasajero=request.user).select_related("taxi__chofer"),
    }
    return render(request, "taxis/viajes/viaje_list.html", contexto)


@rol_requerido(Usuario.Rol.PASAJERO)
def viaje_create(request):
    if request.method == "POST":
        form = ViajeForm(request.POST)
        if form.is_valid():
            viaje = form.save(commit=False)
            viaje.pasajero = request.user
            viaje.save()
            messages.success(request, "Carrera solicitada. Espera a que un chofer la acepte.")
            return redirect("viaje_list")
    else:
        form = ViajeForm()
    return render(request, "taxis/viajes/viaje_form.html", {
        "form": form,
        "encabezado": "Pedir carrera",
    })


@rol_requerido(Usuario.Rol.CHOFER)
@require_POST
def viaje_aceptar(request, pk):
    """El chofer elige una carrera pendiente y la toma."""
    taxi = TaxisFast.objects.filter(chofer=request.user).first()
    if taxi is None:
        messages.error(request, "No tienes un taxi registrado. Habla con el administrador.")
        return redirect("chofer_panel")

    with transaction.atomic():
        viaje = get_object_or_404(Viaje.objects.select_for_update(), pk=pk)
        taxi = TaxisFast.objects.select_for_update().get(pk=taxi.pk)

        if viaje.estado != Viaje.Estado.PENDIENTE:
            messages.error(request, "Esa carrera ya fue tomada por otro chofer.")
        elif taxi.estado != TaxisFast.Estado.EN_BASE:
            messages.error(
                request,
                "Solo puedes aceptar carreras si estás disponible y sin otra carrera en curso.",
            )
        else:
            taxi.estado = TaxisFast.Estado.EN_SERVICIO
            taxi.save(update_fields=["estado"])
            viaje.taxi = taxi
            viaje.estado = Viaje.Estado.ASIGNADO
            viaje.save(update_fields=["taxi", "estado"])
            messages.success(request, "Carrera aceptada. ¡Buen viaje!")
    return redirect("chofer_panel")


@rol_requerido(Usuario.Rol.CHOFER)
@require_POST
def viaje_completar(request, pk):
    """El chofer marca SU carrera como completada y queda libre otra vez."""
    taxi = get_object_or_404(TaxisFast, chofer=request.user)
    with transaction.atomic():
        viaje = get_object_or_404(Viaje.objects.select_for_update(), pk=pk, taxi=taxi)
        if viaje.estado == Viaje.Estado.ASIGNADO:
            viaje.estado = Viaje.Estado.COMPLETADO
            viaje.save(update_fields=["estado"])
            taxi.estado = TaxisFast.Estado.EN_BASE
            taxi.save(update_fields=["estado"])
            messages.success(request, "Viaje completado. Vuelves a estar disponible.")
    return redirect("chofer_panel")
