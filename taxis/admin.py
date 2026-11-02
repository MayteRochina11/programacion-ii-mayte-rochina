# taxis/admin.py
from django.contrib import admin

from .models import Linea, TaxisFast


@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "zona", "created_at")
    search_fields = ("nombre", "zona")


@admin.register(TaxisFast)
class TaxisAdmin(admin.ModelAdmin):
    list_display = ("taxi", "taxi_placa", "taxi_chofer", "taxi_tarifa", "linea", "estado", "taxi_fecha")
    list_filter = ("estado", "linea")
    search_fields = ("taxi", "taxi_placa", "taxi_chofer")
