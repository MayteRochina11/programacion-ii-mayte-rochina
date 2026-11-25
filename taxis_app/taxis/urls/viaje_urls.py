from django.urls import path
from taxis.views.viaje_views import (
    viaje_list, viaje_create, viaje_detail, viaje_update, viaje_delete,
    viaje_aceptar, viaje_completar,
)

urlpatterns = [
    path('viajes/', viaje_list, name='viaje_list'),
    path('viajes/nuevo/', viaje_create, name='viaje_create'),
    path('viajes/<int:pk>/', viaje_detail, name='viaje_detail'),
    path('viajes/<int:pk>/editar/', viaje_update, name='viaje_update'),
    path('viajes/<int:pk>/eliminar/', viaje_delete, name='viaje_delete'),
    path('viajes/<int:pk>/aceptar/', viaje_aceptar, name='viaje_aceptar'),
    path('viajes/<int:pk>/completar/', viaje_completar, name='viaje_completar'),
]
