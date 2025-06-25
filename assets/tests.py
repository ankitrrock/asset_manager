from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from .models import Asset

class RunChecksTest(APITestCase):
    def test_notification_and_violation(self):
        now = timezone.now()
        asset = Asset.objects.create(
            name="TestAsset",
            service_time=now + timedelta(minutes=10),
            expiration_time=now + timedelta(minutes=10),
            is_serviced=False
        )
        response = self.client.post('/api/run-checks/')
        self.assertEqual(response.status_code, 200)
