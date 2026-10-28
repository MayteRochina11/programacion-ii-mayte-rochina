# tasks/admin.py
from django.contrib import admin
from .models import Project, ProjectTaxi, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(ProjectTaxi)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("taxi", "taxi_placa", "taxi_chofer", "taxi_tarifa", "taxi_fecha")
    search_fields = ("taxi",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "due_date")
    list_filter = ("status", "project")
    search_fields = ("title", "description")