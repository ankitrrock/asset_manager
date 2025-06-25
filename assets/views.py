from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Asset, Notification, Violation
from .serializers import AssetSerializer

import logging
logger = logging.getLogger(__name__)


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    @action(detail=True, methods=['post'])
    def mark_serviced(self, request, pk=None):
        asset = self.get_object()
        asset.is_serviced = True
        asset.save()
        logger.info(f"Asset marked as serviced: {asset.name} (ID: {asset.id})")
        return Response({'status': f'Asset {asset.name} marked as serviced'})


@api_view(['POST'])
def run_checks(request):
    logger.info("Running service and expiration checks...")
    now = timezone.now()
    upcoming = now + timedelta(minutes=15)
    assets = Asset.objects.all()

    for asset in assets:
        # Notification for upcoming service
        if now <= asset.service_time <= upcoming:
            notification, created = Notification.objects.get_or_create(
                asset=asset,
                message=f"Service due for asset '{asset.name}' at {asset.service_time}"
            )
            if created:
                logger.info(f"Notification created for service: {asset.name} (ID: {asset.id})")

        # Notification for upcoming expiration
        if now <= asset.expiration_time <= upcoming:
            notification, created = Notification.objects.get_or_create(
                asset=asset,
                message=f"Asset '{asset.name}' expires at {asset.expiration_time}"
            )
            if created:
                logger.info(f"Notification created for expiration: {asset.name} (ID: {asset.id})")

        # Violation for overdue service
        if asset.service_time < now and not asset.is_serviced:
            violation, created = Violation.objects.get_or_create(
                asset=asset,
                issue=f"Service overdue for asset '{asset.name}'"
            )
            if created:
                logger.warning(f"Violation (service) logged for: {asset.name} (ID: {asset.id})")

        # Violation for expired asset
        if asset.expiration_time < now:
            violation, created = Violation.objects.get_or_create(
                asset=asset,
                issue=f"Asset '{asset.name}' has expired"
            )
            if created:
                logger.warning(f"Violation (expiration) logged for: {asset.name} (ID: {asset.id})")

    logger.info("Check run completed.")
    return Response({"message": "Checks completed."}, status=status.HTTP_200_OK)
