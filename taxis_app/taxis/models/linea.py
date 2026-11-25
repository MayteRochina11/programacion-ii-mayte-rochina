from django.db import models
from django.urls import reverse

from taxis.models.zona import Zona


class Linea(models.Model):
    nombre = models.CharField(max_length=100)
    zona = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    zonas = models.ManyToManyField(Zona, blank=True, related_name="lineas")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "línea"
        verbose_name_plural = "líneas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("linea_detail", args=[self.pk])
