from django.conf import settings
from django.db import models

from taxis.models.taxi import TaxisFast


class Viaje(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ASIGNADO = "ASIGNADO", "Aceptado por un chofer"
        COMPLETADO = "COMPLETADO", "Completado"

    pasajero = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="viajes_pedidos",
        limit_choices_to={"rol": "PASAJERO"},
    )
    origen = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    taxi = models.ForeignKey(
        TaxisFast,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="viajes",
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "viaje"
        verbose_name_plural = "viajes"
        ordering = ["-created_at"]

    @property
    def chofer(self):
        return self.taxi.chofer if self.taxi else None

    def __str__(self):
        return f"{self.pasajero}: {self.origen} → {self.destino}"
