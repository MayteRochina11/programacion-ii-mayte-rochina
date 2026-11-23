from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from taxis.decorators import rol_requerido
from taxis.forms.viaje_form import ViajeForm
from taxis.models import TaxisFast, Usuario, Viaje


@login_required
@rol_requerido(Usuario.Rol.PASAJERO)
def viaje_list(request):
    """El pasajero ve SOLO sus propias carreras."""
    contexto = {
        "titulo": "Mis viajes",
        "mensaje": "Pide una carrera y un chofer la aceptará.",
        "viajes": Viaje.objects.filter(pasajero=request.user).select_related("taxi__chofer"),
    }
    return render(request, "taxis/viajes/viaje_list.html", contexto)


@login_required
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


@login_required
@rol_requerido(Usuario.Rol.CHOFER)
@require_POST
def viaje_aceptar(request, pk):
    """El chofer elige una carrera pendiente y la toma."""
    taxi = TaxisFast.objects.filter(chofer=request.user).first()
    if taxi is None:
        messages.error(request, "No tienes un taxi registrado. Habla con el administrador.")
        return redirect("chofer_panel")

    with transaction.atomic():
        # Bloqueamos viaje y taxi: si dos choferes aceptan a la vez, solo gana uno.
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


@login_required
@rol_requerido(Usuario.Rol.CHOFER)
@require_POST
def viaje_completar(request, pk):
    """El chofer marca SU carrera como completada y queda libre otra vez."""
    taxi = get_object_or_404(TaxisFast, chofer=request.user)
    with transaction.atomic():
        # taxi=taxi: un chofer no puede completar la carrera de otro (da 404).
        viaje = get_object_or_404(Viaje.objects.select_for_update(), pk=pk, taxi=taxi)
        if viaje.estado == Viaje.Estado.ASIGNADO:
            viaje.estado = Viaje.Estado.COMPLETADO
            viaje.save(update_fields=["estado"])
            taxi.estado = TaxisFast.Estado.EN_BASE
            taxi.save(update_fields=["estado"])
            messages.success(request, "Viaje completado. Vuelves a estar disponible.")
    return redirect("chofer_panel")


@login_required
def viaje_detail(request, pk):
    """Detalle de una carrera: solo para su pasajero, su chofer y el administrador.

    Un chofer también puede ver las carreras pendientes, que son las que puede aceptar.
    """
    viaje = get_object_or_404(
        Viaje.objects.select_related("pasajero", "taxi__chofer", "taxi__linea"), pk=pk
    )
    usuario = request.user
    es_pasajero = viaje.pasajero_id == usuario.pk
    es_chofer_asignado = viaje.taxi_id is not None and viaje.taxi.chofer_id == usuario.pk
    chofer_ve_pendiente = usuario.es_chofer and viaje.estado == Viaje.Estado.PENDIENTE

    if not (usuario.es_admin or es_pasajero or es_chofer_asignado or chofer_ve_pendiente):
        raise Http404  # no revelamos que la carrera existe

    return render(request, "taxis/viajes/viaje_detail.html", {
        "viaje": viaje,
        # Los teléfonos se muestran solo cuando la carrera ya tiene chofer.
        "ver_tel_pasajero": viaje.taxi_id is not None and (usuario.es_admin or es_chofer_asignado),
        "ver_tel_chofer": viaje.taxi_id is not None and (usuario.es_admin or es_pasajero),
    })
