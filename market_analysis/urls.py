from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarketAnalysisViewSet, MarketPriceViewSet, PriceAlertViewSet

router = DefaultRouter()
router.register(r'analysis', MarketAnalysisViewSet, basename='market-analysis')
router.register(r'prices', MarketPriceViewSet, basename='market-prices')
router.register(r'alerts', PriceAlertViewSet, basename='price-alerts')

urlpatterns = [
    path('', include(router.urls)),
]
