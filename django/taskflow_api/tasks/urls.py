from django.urls import path
from . import views

app_name = "tasks"   # namespace de la app — ver nota más abajo

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("perfil", views.perfil, name="perfil"),
    path("aboutme", views.about_me, name="about_me"),
    path("saludo/<str:nombre>/", views.greeting, name="saludo"),
    path("destination/<str:titulo>/<str:nombre>/<str:cargo>/",
         views.destination, name="destination"),
    path("my-first-template", views.my_first_template, name="my-first-template.html")
]