from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render

from taxis.models import TaxisFast, Viaje


@login_required
@permission_required("taxis.view_taxisfast", raise_exception=True)
def taxi_list(request):
    contexto = {
        "titulo": "Flota",
        "mensaje": "Los taxis de TaxisFast.",
        "taxis": TaxisFast.objects.select_related("chofer", "linea"),
    }
    return render(request, "taxis/flota/taxi_list.html", contexto)


@login_required
@permission_required("taxis.view_taxisfast", raise_exception=True)
def taxi_detail(request, pk):
    taxi = get_object_or_404(TaxisFast.objects.select_related("chofer", "linea"), pk=pk)
    es_dueno = taxi.chofer_id == request.user.pk
    viajes = Viaje.objects.none()
    if es_dueno or request.user.es_admin:
        viajes = taxi.viajes.select_related("creado_por")[:10]
    return render(request, "taxis/flota/taxi_detail.html", {
        "taxi": taxi,
        "es_dueno": es_dueno,
        "viajes": viajes,
        "viajes_completados": taxi.viajes.filter(estado=Viaje.Estado.COMPLETADO).count(),
    })
