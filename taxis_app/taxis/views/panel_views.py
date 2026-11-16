from django.db.models import Count, Q
from django.shortcuts import render

from taxis.decorators import rol_requerido
from taxis.models import Linea, TaxisFast, Usuario, Viaje


@rol_requerido(Usuario.Rol.ADMIN)
def panel_admin(request):
    """Resumen general para el administrador."""
    contexto = {
        "titulo": "Panel del administrador",
        "total_choferes": Usuario.objects.filter(rol=Usuario.Rol.CHOFER).count(),
        "total_pasajeros": Usuario.objects.filter(rol=Usuario.Rol.PASAJERO).count(),
        "total_lineas": Linea.objects.count(),
        "taxis_en_base": TaxisFast.objects.filter(estado=TaxisFast.Estado.EN_BASE).count(),
        "taxis_en_servicio": TaxisFast.objects.filter(estado=TaxisFast.Estado.EN_SERVICIO).count(),
        "taxis_fuera": TaxisFast.objects.filter(estado=TaxisFast.Estado.FUERA_DE_SERVICIO).count(),
        "viajes_pendientes": Viaje.objects.filter(estado=Viaje.Estado.PENDIENTE).count(),
        "viajes_asignados": Viaje.objects.filter(estado=Viaje.Estado.ASIGNADO).count(),
        "viajes_completados": Viaje.objects.filter(estado=Viaje.Estado.COMPLETADO).count(),
    }
    return render(request, "taxis/panel/panel_admin.html", contexto)


@rol_requerido(Usuario.Rol.ADMIN)
def panel_choferes(request):
    choferes = (
        Usuario.objects.filter(rol=Usuario.Rol.CHOFER)
        .select_related("vehiculo__linea")
        .annotate(
            viajes_completados=Count(
                "vehiculo__viajes",
                filter=Q(vehiculo__viajes__estado=Viaje.Estado.COMPLETADO),
            )
        )
        .order_by("first_name", "username")
    )
    return render(request, "taxis/panel/panel_choferes.html", {
        "titulo": "Choferes",
        "choferes": choferes,
    })


@rol_requerido(Usuario.Rol.ADMIN)
def panel_pasajeros(request):
    pasajeros = (
        Usuario.objects.filter(rol=Usuario.Rol.PASAJERO)
        .annotate(total_viajes=Count("viajes_pedidos"))
        .order_by("first_name", "username")
    )
    return render(request, "taxis/panel/panel_pasajeros.html", {
        "titulo": "Pasajeros",
        "pasajeros": pasajeros,
    })


@rol_requerido(Usuario.Rol.ADMIN)
def panel_viajes(request):
    return render(request, "taxis/panel/panel_viajes.html", {
        "titulo": "Todos los viajes",
        "viajes": Viaje.objects.select_related("pasajero", "taxi__chofer"),
    })
