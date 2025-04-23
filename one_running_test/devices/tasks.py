from celery import shared_task
from .models import Training, Device
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def sync_trainings():
    """Tarea en segundo plano que sincroniza entrenamientos desde los dispositivos autorizados."""
    logger.info("Iniciando sincronización de entrenamientos...")

    try:
        # Obtener solo dispositivos autorizados
        authorized_devices = Device.objects.filter(authorized=True)

        for device in authorized_devices:
            logger.info(f"Sincronizando datos para dispositivo {device.device_id}")

            # Lógica simulada de sincronización
            Training.objects.create(
                device=device,
                start_time=timezone.now(),
                duration=3600,  # 1 hora
                distance=10.5  # 10.5 km ficticios
            )

        logger.info("Sincronización completada exitosamente")
        return "Sincronización completada exitosamente"

    except Exception as e:
        logger.error(f"Error en sincronización: {str(e)}")
        return f"Error en sincronización: {str(e)}"
@shared_task
def sync_training_data(device_id):
    print(f"[CELERY] Sincronizando datos para {device_id}")
    return f"Sincronización completada para dispositivo {device_id}"
