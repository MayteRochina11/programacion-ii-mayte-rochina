from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from taxis.models.linea import Linea


class TaxisFast(models.Model):
    class Estado(models.TextChoices):
        EN_BASE = "EN_BASE", "En la base"
        EN_SERVICIO = "EN_SERVICIO", "En servicio"
        FUERA_DE_SERVICIO = "FUERA_DE_SERVICIO", "Fuera de servicio"

    chofer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vehiculo",
        limit_choices_to={"rol": "CHOFER"},
    )
    linea = models.ForeignKey(
        Linea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="taxis",
    )
    taxi = models.CharField(max_length=100)
    taxi_placa = models.TextField(blank=True)
    taxi_fecha = models.DateTimeField(auto_now_add=True)
    taxi_tarifa = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.EN_BASE,
    )

    class Meta:
        verbose_name = "taxi"
        verbose_name_plural = "taxis"
        ordering = ["taxi"]

    def __str__(self):
        return self.taxi

    def get_absolute_url(self):
        return reverse("taxi_detail", args=[self.pk])
