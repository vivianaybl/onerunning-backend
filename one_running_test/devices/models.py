from django.db import models
from django.core.exceptions import ValidationError

class Device(models.Model):
    class Meta:
        db_table = 'devices_device'
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'

    id = models.BigAutoField(primary_key=True)
    user_email = models.EmailField(max_length=254)
    device_id = models.CharField(
        max_length=100,
        unique=True,
        editable=False
    )
    auth_token = models.TextField()
    authorized = models.BooleanField(default=False)  # Cambio de nombre para más claridad

    def save(self, *args, **kwargs):
        if not self.device_id:
            last_device = Device.objects.order_by('-id').first()
            last_id = 0
            if last_device and last_device.device_id.startswith("dev_"):
                try:
                    last_id = int(last_device.device_id.split('_')[1])
                except (IndexError, ValueError):
                    pass
            next_id = last_id + 1
            proposed_id = f"dev_{next_id}"
            while Device.objects.filter(device_id=proposed_id).exists():
                next_id += 1
                proposed_id = f"dev_{next_id}"
            self.device_id = proposed_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.device_id} ({self.user_email})"


class Training(models.Model):
    class Meta:
        db_table = 'training'
        verbose_name = 'Entrenamiento'
        verbose_name_plural = 'Entrenamientos'

    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        db_column='device_id'
    )
    start_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duración en segundos")
    distance = models.FloatField(null=True, help_text="Distancia en km")

    def __str__(self):
        return f"Entrenamiento {self.id} - {self.start_time}"
