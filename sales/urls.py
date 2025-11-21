from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PaymentMethodViewSet, CustomerViewSet, OrderViewSet, 
                    OrderItemViewSet, PaymentViewSet)

router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-method')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
