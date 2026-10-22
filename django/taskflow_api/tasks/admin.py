# tasks/admin.py
from django.contrib import admin
from .models import Project, ProjectTaxi


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(ProjectTaxi)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("taxi", "taxi_placa", "taxi_chofer", "taxi_tarifa", "taxi_fecha")
    search_fields = ("taxi",)
