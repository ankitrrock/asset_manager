from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Asset, Notification, Violation

class AssetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.now = timezone.now()
        self.asset = Asset.objects.create(
            name="Test Asset",
            service_time=self.now + timedelta(minutes=10),
            expiration_time=self.now + timedelta(minutes=10),
            is_serviced=False
        )

    def test_create_asset(self):
        response = self.client.post('/api/assets/', {
            "name": "New Asset",
            "service_time": str(self.now + timedelta(minutes=20)),
            "expiration_time": str(self.now + timedelta(minutes=30)),
            "is_serviced": False
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_run_checks_creates_notification(self):
        response = self.client.post('/api/run-checks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notifications = Notification.objects.filter(asset=self.asset)
        self.assertTrue(notifications.exists(), "Notification should be created within 15 mins")

    def test_run_checks_creates_violation(self):
        self.asset.service_time = self.now - timedelta(minutes=30)
        self.asset.expiration_time = self.now - timedelta(minutes=10)
        self.asset.save()
        response = self.client.post('/api/run-checks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        violations = Violation.objects.filter(asset=self.asset)
        self.assertTrue(violations.exists(), "Violation should be created if service is overdue or asset expired")

    def test_mark_asset_as_serviced(self):
        response = self.client.post(f'/api/assets/{self.asset.id}/mark_serviced/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.asset.refresh_from_db()
        self.assertTrue(self.asset.is_serviced)

    def test_invalid_service_time_validation(self):
        response = self.client.post('/api/assets/', {
            "name": "Invalid Asset",
            "service_time": str(self.now + timedelta(minutes=30)),
            "expiration_time": str(self.now + timedelta(minutes=10)),
            "is_serviced": False
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
