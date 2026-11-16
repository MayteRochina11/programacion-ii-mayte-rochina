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
