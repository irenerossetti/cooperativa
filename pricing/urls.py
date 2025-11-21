from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PriceListViewSet, PriceListItemViewSet

router = DefaultRouter()
router.register(r'price-lists', PriceListViewSet, basename='price-list')
router.register(r'price-list-items', PriceListItemViewSet, basename='price-list-item')

urlpatterns = [
    path('', include(router.urls)),
]
