from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from taxis.forms.viaje_form import ViajeForm
from taxis.models import TaxisFast, Viaje


def puede_modificar_viaje(usuario, viaje):
    if usuario.es_admin:
        return True
    return viaje.creado_por_id == usuario.pk and viaje.estado == Viaje.Estado.PENDIENTE


def _volver(usuario):
    return redirect("panel_viajes" if usuario.es_admin else "viaje_list")


@login_required
@permission_required("taxis.add_viaje", raise_exception=True)
def viaje_list(request):
    contexto = {
        "titulo": "Mis viajes",
        "mensaje": "Pide una carrera y un chofer la aceptará.",
        "viajes": Viaje.objects.filter(creado_por=request.user).select_related("taxi__chofer"),
    }
    return render(request, "taxis/viajes/viaje_list.html", contexto)


@login_required
@permission_required("taxis.view_viaje", raise_exception=True)
def viaje_detail(request, pk):
    viaje = get_object_or_404(
        Viaje.objects.select_related("creado_por", "taxi__chofer", "taxi__linea"), pk=pk
    )
    usuario = request.user
    es_pasajero = viaje.creado_por_id == usuario.pk
    es_chofer_asignado = viaje.taxi_id is not None and viaje.taxi.chofer_id == usuario.pk
    chofer_ve_pendiente = usuario.es_chofer and viaje.estado == Viaje.Estado.PENDIENTE

    if not (usuario.es_admin or es_pasajero or es_chofer_asignado or chofer_ve_pendiente):
        raise Http404

    return render(request, "taxis/viajes/viaje_detail.html", {
        "viaje": viaje,
        "puede_modificar": puede_modificar_viaje(usuario, viaje),
        "ver_tel_pasajero": viaje.taxi_id is not None and (usuario.es_admin or es_chofer_asignado),
        "ver_tel_chofer": viaje.taxi_id is not None and (usuario.es_admin or es_pasajero),
    })


@login_required
@permission_required("taxis.add_viaje", raise_exception=True)
def viaje_create(request):
    if request.method == "POST":
        form = ViajeForm(request.POST)
        if form.is_valid():
            viaje = form.save(commit=False)
            viaje.creado_por = request.user
            viaje.save()
            messages.success(request, "Carrera solicitada. Espera a que un chofer la acepte.")
            return _volver(request.user)
    else:
        form = ViajeForm()
    return render(request, "taxis/viajes/viaje_form.html", {
        "form": form,
        "encabezado": "Pedir carrera",
        "cancelar_url": "viaje_list",
    })


@login_required
@permission_required("taxis.change_viaje", raise_exception=True)
def viaje_update(request, pk):
    viaje = get_object_or_404(Viaje, pk=pk)
    if not puede_modificar_viaje(request.user, viaje):
        raise PermissionDenied
    if request.method == "POST":
        form = ViajeForm(request.POST, instance=viaje)
        if form.is_valid():
            form.save()
            messages.success(request, "Carrera actualizada exitosamente.")
            return _volver(request.user)
    else:
        form = ViajeForm(instance=viaje)
    return render(request, "taxis/viajes/viaje_form.html", {
        "form": form,
        "encabezado": "Editar carrera",
        "cancelar_url": "panel_viajes" if request.user.es_admin else "viaje_list",
    })


@login_required
@permission_required("taxis.delete_viaje", raise_exception=True)
def viaje_delete(request, pk):
    viaje = get_object_or_404(Viaje, pk=pk)
    if not puede_modificar_viaje(request.user, viaje):
        raise PermissionDenied
    if request.method == "POST":
        with transaction.atomic():
            if viaje.estado == Viaje.Estado.ASIGNADO and viaje.taxi:
                viaje.taxi.estado = TaxisFast.Estado.EN_BASE
                viaje.taxi.save(update_fields=["estado"])
            viaje.delete()
        messages.success(request, "Carrera eliminada exitosamente.")
        return _volver(request.user)
    return render(request, "taxis/viajes/viaje_confirm_delete.html", {
        "viaje": viaje,
        "cancelar_url": viaje.get_absolute_url(),
    })


@login_required
@permission_required("taxis.aceptar_viaje", raise_exception=True)
@require_POST
def viaje_aceptar(request, pk):
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


@login_required
@permission_required("taxis.completar_viaje", raise_exception=True)
@require_POST
def viaje_completar(request, pk):
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
