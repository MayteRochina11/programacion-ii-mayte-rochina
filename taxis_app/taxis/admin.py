from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from taxis.models import Linea, TaxisFast, Usuario, Viaje, Zona


class UsuarioCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = Usuario
        fields = ("username", "first_name", "last_name", "telefono", "rol")


class UsuarioChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm
    list_display = ("username", "first_name", "last_name", "rol", "telefono", "is_active")
    list_filter = ("rol", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Rol en TaxisFast", {"fields": ("rol", "telefono")}),)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "usable_password", "password1", "password2"),
        }),
        ("Datos", {"fields": ("first_name", "last_name", "telefono", "rol")}),
    )


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion", "created_at")
    list_filter = ("created_at",)
    search_fields = ("nombre", "descripcion")


@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "zona", "created_at")
    list_filter = ("zonas",)
    search_fields = ("nombre", "zona")
    filter_horizontal = ("zonas",)


@admin.register(TaxisFast)
class TaxisAdmin(admin.ModelAdmin):
    list_display = ("taxi", "taxi_placa", "chofer", "taxi_tarifa", "linea", "estado", "taxi_fecha")
    list_filter = ("estado", "linea")
    search_fields = ("taxi", "taxi_placa", "chofer__username", "chofer__first_name")


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ("creado_por", "origen", "destino", "taxi", "estado", "created_at")
    list_filter = ("estado",)
    search_fields = ("creado_por__username", "creado_por__first_name", "origen", "destino")
