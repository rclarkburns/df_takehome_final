from rest_framework import serializers
from dashfuel.tanks.models import Tank, TankVolume


class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = ['id', 'name']


class TankVolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TankVolume
        fields = ['id', 'tank', 'volume', 'created_at']
