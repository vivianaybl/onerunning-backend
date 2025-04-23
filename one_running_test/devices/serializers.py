from rest_framework import serializers
from .models import Device, Training

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_id', 'user_email', 'auth_token', 'authorized']
        read_only_fields = ['device_id']  # El sistema lo genera automáticamente

    def validate_user_email(self, value):
        if Device.objects.filter(user_email=value, authorized=True).exists():
            raise serializers.ValidationError("Ya existe un dispositivo autorizado con este email.")
        return value


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'
