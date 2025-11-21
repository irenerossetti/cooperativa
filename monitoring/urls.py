from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CropMonitoringViewSet, CropAlertViewSet

router = DefaultRouter()
router.register(r'monitoring', CropMonitoringViewSet, basename='crop-monitoring')
router.register(r'alerts', CropAlertViewSet, basename='crop-alert')

urlpatterns = [
    path('', include(router.urls)),
]
