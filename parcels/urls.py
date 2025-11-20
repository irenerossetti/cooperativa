from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParcelViewSet, SoilTypeViewSet, CropViewSet

router = DefaultRouter()
router.register(r'parcels', ParcelViewSet, basename='parcel')
router.register(r'soil-types', SoilTypeViewSet, basename='soil-type')
router.register(r'crops', CropViewSet, basename='crop')

urlpatterns = [
    path('', include(router.urls)),
]
