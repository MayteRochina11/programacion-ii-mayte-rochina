from django.urls import path
from taxis.views.linea_views import (linea_list, linea_create)

urlpatterns = [
    path('lineas/', linea_list, name='linea_list'),
    path('lineas/nueva/', linea_create, name='linea_create'),
]
