# taxis/urls.py
from django.urls import path

from . import views

app_name = "taxis"  # namespace: se usa como {% url 'taxis:home' %}

urlpatterns = [
    path("", views.taxi_lista, name="home"),
    path("nuevo/", views.taxi_create, name="taxi_create"),
    path("lineas/", views.lineas_lista, name="lineas_lista"),
    path("lineas/nueva/", views.linea_create, name="linea_create"),
    path("sobre-nosotros/", views.sobre_nosotros, name="sobre_nosotros"),
]
