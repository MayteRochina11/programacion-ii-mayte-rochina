from django.shortcuts import redirect, render

from taxis.models import Usuario


PANEL_POR_ROL = {
    Usuario.Rol.PASAJERO: "viaje_list",
    Usuario.Rol.CHOFER: "chofer_panel",
    Usuario.Rol.ADMIN: "panel_admin",
}


def inicio(request):

    if request.user.is_authenticated:
        return redirect(PANEL_POR_ROL[request.user.rol])
    contexto = {
        "titulo": "TaxisFast",
        "mensaje": "Tu taxi de confianza mas rapido del mercado",
    }
    return render(request, "taxis/general/inicio.html", contexto)


def sobre_nosotros(request):
    contexto = {
        "titulo": "Sobre TaxisFast",
        "mensaje": "Conoce un poco más sobre nuestra misión y visión.",
    }
    return render(request, "taxis/general/sobre_nosotros.html", contexto)
