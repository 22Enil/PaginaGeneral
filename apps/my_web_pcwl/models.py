from django.db import models

# Create your models here.
class Productos(models.Model):
    precio = models.FloatField(default=0.0)
    stok = models.IntegerField(default=0)
    nombre = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Nombre producto {self.nombre}"
