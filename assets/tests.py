from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Asset, Notification, Violation

class AssetTestCase(APITestCase):

    def setUp(self):
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
        self.client.post('/api/run-checks/')
        notifications = Notification.objects.filter(asset=self.asset)
        self.assertTrue(notifications.exists(), "Notification should be created within 15 mins")

    def test_run_checks_creates_violation(self):
        # Set past times
        self.asset.service_time = self.now - timedelta(minutes=30)
        self.asset.expiration_time = self.now - timedelta(minutes=10)
        self.asset.save()

        self.client.post('/api/run-checks/')
        violations = Violation.objects.filter(asset=self.asset)
        self.assertTrue(violations.exists(), "Violation should be created if service is overdue or asset expired")

    def test_mark_asset_as_serviced(self):
        response = self.client.post(f'/api/assets/{self.asset.id}/mark_serviced/')
        self.asset.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.asset.is_serviced)

    def test_invalid_service_time_validation(self):
        response = self.client.post('/api/assets/', {
            "name": "Invalid Asset",
            "service_time": str(self.now + timedelta(minutes=30)),
            "expiration_time": str(self.now + timedelta(minutes=10)),
            "is_serviced": False
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
