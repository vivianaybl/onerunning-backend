from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, TrainingViewSet, authorize_device, trigger_sync

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'trainings', TrainingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/devices/authorize/', authorize_device, name='authorize-device'),
    path('api/trainings/sync/', trigger_sync, name='sync-trainings') ,
    path('authorize_device/', authorize_device, name='authorize-device'),
    path('trigger_sync/', trigger_sync, name='trigger-sync')
]