from django.urls import path
from taxis.views.viaje_views import (
    viaje_list, viaje_create, viaje_aceptar, viaje_completar,
)

urlpatterns = [
    path('viajes/', viaje_list, name='viaje_list'),
    path('viajes/nuevo/', viaje_create, name='viaje_create'),
    path('viajes/<int:pk>/aceptar/', viaje_aceptar, name='viaje_aceptar'),
    path('viajes/<int:pk>/completar/', viaje_completar, name='viaje_completar'),
]
