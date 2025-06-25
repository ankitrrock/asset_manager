from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssetViewSet, run_checks

router = DefaultRouter()
router.register('assets', AssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('run-checks/', run_checks),
]
