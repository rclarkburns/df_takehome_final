from django.db import models


class Tank(models.Model):
    name = models.CharField(max_length=255)
