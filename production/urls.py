from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HarvestedProductViewSet

router = DefaultRouter()
router.register(r'harvested-products', HarvestedProductViewSet, basename='harvested-product')

urlpatterns = [
    path('', include(router.urls)),
]
