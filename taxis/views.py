from django.shortcuts import render

# Create your views here.
def taxi_view(request):
    contexto = {
        "titulo": "TaxisFast",
        "mensaje": "Tu taxi de confianza mas rapido del mercado",
    }
    return render(request, "taxis/taxis.html", contexto)

def sobre_nosotros(request):
    contexto = {
        "titulo": "Sobre TaxisFast",
        "mensaje": "Conoce un poco más sobre nuestra misión y visión.",
    }
    return render(request, "taxis/sobre_nosotros.html", contexto)
 