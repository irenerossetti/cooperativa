from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParcelTraceabilityViewSet, InputUsageRecordViewSet

router = DefaultRouter()
router.register(r'parcels', ParcelTraceabilityViewSet, basename='parcel-traceability')
router.register(r'input-usage', InputUsageRecordViewSet, basename='input-usage')

urlpatterns = [
    path('', include(router.urls)),
]
