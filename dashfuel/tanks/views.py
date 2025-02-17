from django.shortcuts import render
from rest_framework import viewsets
from dashfuel.tanks.models import Tank, TankVolume
from dashfuel.tanks.serializers import TankSerializer, TankVolumeSerializer


class TankViewSet(viewsets.ModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer


class TankVolumeViewSet(viewsets.ModelViewSet):
    queryset = TankVolume.objects.all()
    serializer_class = TankVolumeSerializer
