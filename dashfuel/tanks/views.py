from rest_framework import viewsets
from dashfuel.tanks.models import Tank, TankVolume, WeeklyTankSales
from dashfuel.tanks.serializers import TankSerializer, TankVolumeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime


class TankViewSet(viewsets.ModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer


class TankVolumeViewSet(viewsets.ModelViewSet):
    queryset = TankVolume.objects.all()
    serializer_class = TankVolumeSerializer


@api_view(['GET'])
def average_sales(request):
    date_str = request.GET.get('date')

    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)

    average = WeeklyTankSales.get_average_sales(target_date)

    return Response({
        'target_week_end': target_date,
        'average_sales': average
    })

