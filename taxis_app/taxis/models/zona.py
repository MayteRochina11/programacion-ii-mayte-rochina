from django.db import models
from django.urls import reverse


class Zona(models.Model):
    """Sector o barrio de la ciudad. Una línea cubre varias zonas y una zona la cubren varias líneas."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "zona"
        verbose_name_plural = "zonas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("zona_detail", args=[self.pk])
