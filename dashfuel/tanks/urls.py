from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dashfuel.tanks.views import TankViewSet, TankVolumeViewSet

router = DefaultRouter()
router.register(r'tanks', TankViewSet)
router.register(r'tank-volumes', TankVolumeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
