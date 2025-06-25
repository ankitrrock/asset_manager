from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Asset, Notification, Violation
from .serializers import AssetSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    @action(detail=True, methods=['post'])
    def mark_serviced(self, request, pk=None):
        asset = self.get_object()
        asset.is_serviced = True
        asset.save()
        return Response({'status': f'Asset {asset.name} marked as serviced'})

@api_view(['POST'])
def run_checks(request):
    now = timezone.now()
    upcoming = now + timedelta(minutes=15)
    assets = Asset.objects.all()

    for asset in assets:
        if now <= asset.service_time <= upcoming:
            Notification.objects.get_or_create(
                asset=asset,
                message=f"Service due for asset '{asset.name}' at {asset.service_time}"
            )
        if now <= asset.expiration_time <= upcoming:
            Notification.objects.get_or_create(
                asset=asset,
                message=f"Asset '{asset.name}' expires at {asset.expiration_time}"
            )
        if asset.service_time < now and not asset.is_serviced:
            Violation.objects.get_or_create(
                asset=asset,
                issue=f"Service overdue for asset '{asset.name}'"
            )
        if asset.expiration_time < now:
            Violation.objects.get_or_create(
                asset=asset,
                issue=f"Asset '{asset.name}' has expired"
            )

    return Response({"message": "Checks completed."}, status=status.HTTP_200_OK)
