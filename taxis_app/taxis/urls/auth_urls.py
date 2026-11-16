from django.urls import path
from taxis.views.auth_views import (
    ingresar, salir, registro_pasajero, registro_chofer,
)

urlpatterns = [
    path('ingresar/', ingresar, name='ingresar'),
    path('salir/', salir, name='salir'),
    path('registro/pasajero/', registro_pasajero, name='registro_pasajero'),
    path('registro/chofer/', registro_chofer, name='registro_chofer'),
]
