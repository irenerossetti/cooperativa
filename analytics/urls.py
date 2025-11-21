from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PriceTrendViewSet, DemandTrendViewSet

router = DefaultRouter()
router.register(r'price-trends', PriceTrendViewSet, basename='price-trend')
router.register(r'demand-trends', DemandTrendViewSet, basename='demand-trend')

urlpatterns = [
    path('', include(router.urls)),
]
