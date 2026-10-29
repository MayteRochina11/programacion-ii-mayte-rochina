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
    path("base_triangulo/<int:base>/<int:altura>/",
         views.base_triangulo, name="base_triangulo"),
    path("my-first-template", views.my_first_template, name="my-first-template.html"),
    path("leads-like", views.leads_like, name="leads-like"),
    path("projects/lista", 
                         views.project_lista,
                         name="project-lista"),
     #"path("tasks/new/", views.task_create, name="task_create"),"
     path("projects/new/", views.project_create, name="project_create"),
]