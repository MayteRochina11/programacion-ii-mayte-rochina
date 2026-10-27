# tasks/models.py
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectTaxi(models.Model):
    taxi = models.CharField(max_length=100)
    taxi_placa = models.TextField(blank=True)
    taxi_fecha = models.DateTimeField(auto_now_add=True)
    taxi_chofer = models.TextField(blank=True)
    taxi_tarifa = models.TextField(blank=True)

    def __str__(self):
        return self.taxi

