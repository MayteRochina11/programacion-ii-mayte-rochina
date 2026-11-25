from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse


GRUPO_POR_ROL = {
    "PASAJERO": "pasajeros",
    "CHOFER": "choferes",
    "ADMIN": "administradores",
}


class UsuarioManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        if self.filter(rol=Usuario.Rol.ADMIN).exists():
            raise ValidationError("Ya existe un administrador. Solo puede haber uno.")
        extra_fields["rol"] = Usuario.Rol.ADMIN
        return super().create_superuser(username, email, password, **extra_fields)


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        PASAJERO = "PASAJERO", "Pasajero"
        CHOFER = "CHOFER", "Chofer"
        ADMIN = "ADMIN", "Administrador"

    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.PASAJERO)
    telefono = models.CharField(max_length=20, blank=True)

    objects = UsuarioManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["username"]
        constraints = [
            models.UniqueConstraint(
                fields=["rol"],
                condition=Q(rol="ADMIN"),
                name="un_solo_administrador",
                violation_error_message="Ya existe un administrador. Solo puede haber uno.",
            ),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sincronizar_grupo()

    def sincronizar_grupo(self):
        destino = GRUPO_POR_ROL[self.rol]
        grupos = {g.name: g for g in Group.objects.filter(name__in=GRUPO_POR_ROL.values())}
        self.groups.remove(*[g for nombre, g in grupos.items() if nombre != destino])
        if destino in grupos:
            self.groups.add(grupos[destino])

    @property
    def es_admin(self):
        return self.rol == self.Rol.ADMIN

    @property
    def es_chofer(self):
        return self.rol == self.Rol.CHOFER

    @property
    def es_pasajero(self):
        return self.rol == self.Rol.PASAJERO

    @property
    def nombre_completo(self):
        return self.get_full_name() or self.username

    def get_absolute_url(self):
        return reverse("inicio")

    def __str__(self):
        return self.nombre_completo
