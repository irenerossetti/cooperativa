from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (InventoryItemViewSet, InventoryMovementViewSet,
                    InventoryCategoryViewSet, StockAlertViewSet)

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet, basename='inventory-item')
router.register(r'movements', InventoryMovementViewSet, basename='inventory-movement')
router.register(r'categories', InventoryCategoryViewSet, basename='inventory-category')
router.register(r'alerts', StockAlertViewSet, basename='stock-alert')

urlpatterns = [
    path('', include(router.urls)),
]
