from django.contrib import admin
from .models import TaxisFast

# Register your models here.
@admin.register(TaxisFast)
class TaxisAdmin(admin.ModelAdmin):
    list_display = ("taxi", "taxi_placa", "taxi_chofer", "taxi_tarifa", "taxi_fecha")
    search_fields = ("taxi",)