from django.db import models

# Create your models here.
class TaxisFast(models.Model):
    taxi = models.CharField(max_length=100)
    taxi_placa = models.TextField(blank=True)
    taxi_fecha = models.DateTimeField(auto_now_add=True)
    taxi_chofer = models.TextField(blank=True)
    taxi_tarifa = models.TextField(blank=True)

    def __str__(self):
        return self.taxi

### Para hacer pr
