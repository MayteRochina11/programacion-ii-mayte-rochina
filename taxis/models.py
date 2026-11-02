# taxis/models.py
from django.db import models


class Linea(models.Model):
    nombre = models.CharField(max_length=100)
    zona = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "línea"
        verbose_name_plural = "líneas"

    def __str__(self):
        return self.nombre


class TaxisFast(models.Model):
    class Estado(models.TextChoices):
        EN_BASE = "EN_BASE", "En la base"
        EN_SERVICIO = "EN_SERVICIO", "En servicio"
        FUERA_DE_SERVICIO = "FUERA_DE_SERVICIO", "Fuera de servicio"

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
    taxi_chofer = models.TextField(blank=True)
    taxi_tarifa = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.EN_BASE,
    )

    def __str__(self):
        return self.taxi
