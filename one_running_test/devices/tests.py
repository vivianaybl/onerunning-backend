from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from devices.models import Device, Training
from django.utils import timezone
from devices.tasks import sync_trainings

class APITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_device_authorization(self):
        """Autoriza un dispositivo correctamente"""
        data = {
            "user_email": "viviana@test.com",
            "auth_token": "abc123",
            "authorized": True
        }
        response = self.client.post(reverse('authorize-device'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("device_id", response.data)
        self.assertTrue(Device.objects.filter(user_email="viviana@test.com").exists())

    def test_device_duplicate_authorization(self):
        """Evita autorizar más de un dispositivo para el mismo email"""
        Device.objects.create(user_email="viviana@test.com", auth_token="tok1", authorized=True)
        data = {
            "user_email": "viviana@test.com",
            "auth_token": "tok2",
            "authorized": True
        }
        response = self.client.post(reverse('authorize-device'), data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_trigger_sync_task(self):
        """Verifica que se pueda disparar la tarea de sincronización"""
        response = self.client.post(reverse('trigger-sync'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Synchronization started")

    def test_training_creation(self):
        """Crea un entrenamiento asociado a un dispositivo"""
        device = Device.objects.create(user_email="test@test.com", auth_token="tok", authorized=True)
        training = Training.objects.create(
            device=device,
            start_time=timezone.now(),
            duration=1800,
            distance=5.0
        )
        self.assertEqual(training.device.device_id, device.device_id)

    def test_sync_task_creates_training(self):
        """Verifica que la tarea de sincronización crea entrenamientos"""
        device = Device.objects.create(user_email="sync@test.com", auth_token="tok", authorized=True)
        sync_trainings()
        self.assertEqual(Training.objects.filter(device=device).count(), 1)

    def test_authorize_device(self):
        print("[TEST] Probando autorización de dispositivo")
        response = self.client.post('/devices/authorize/', {'device_id': '123abc'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

