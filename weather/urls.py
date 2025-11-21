from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherDataViewSet, WeatherForecastViewSet, WeatherAlertViewSet

router = DefaultRouter()
router.register(r'data', WeatherDataViewSet, basename='weather-data')
router.register(r'forecast', WeatherForecastViewSet, basename='weather-forecast')
router.register(r'alerts', WeatherAlertViewSet, basename='weather-alert')

urlpatterns = [
    path('', include(router.urls)),
]
