from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tanks', views.TankViewSet)
router.register(r'tank-volumes', views.TankVolumeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('average-sales/', views.average_sales, name='average-sales'),
]