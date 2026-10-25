from django.urls import path
from . import views

app_name = 'taxis'

urlpatterns = [
    path("", views.taxi_view, name="home"),
    path("sobre-nosotros/", views.sobre_nosotros, name="sobre_nosotros"),
]