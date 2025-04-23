from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import sync_trainings as celery_sync_trainings  # Renombramos para evitar conflicto
from .models import Device, Training
from .serializers import DeviceSerializer, TrainingSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

@api_view(['POST'])
def authorize_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        device = serializer.save()
        return Response({
            "status": "success",
            "device_id": device.device_id,
            "message": "Dispositivo autorizado"
        })
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def trigger_sync(request):  # Cambiamos el nombre para mayor claridad
    """Endpoint para disparar la sincronización"""
    celery_sync_trainings.delay()
    return Response({"status": "Synchronization started"})

def post(self, request):
    device_id = request.data.get('device_id')
    print(f"[DEBUG] Autorizando dispositivo: {device_id}")
    sync_training_data.delay(device_id)
    return Response({"message": "Dispositivo autorizado"}, status=status.HTTP_200_OK)
