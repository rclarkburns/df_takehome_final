from django.db import models
from django.utils import timezone


class Tank(models.Model):
    name = models.CharField(max_length=255)


class TankVolume(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    volume = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now())
