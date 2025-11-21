from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import WeatherData, WeatherForecast, WeatherAlert
from .serializers import WeatherDataSerializer, WeatherForecastSerializer, WeatherAlertSerializer
import requests
from django.conf import settings
from datetime import datetime, timedelta


class WeatherDataViewSet(viewsets.ModelViewSet):
    """ViewSet para datos climáticos"""
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['community', 'date']
    ordering_fields = ['date', 'time']
    ordering = ['-date', '-time']

    @action(detail=False, methods=['post'])
    def fetch_current(self, request):
        """Obtener datos climáticos actuales desde API"""
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        community_id = request.data.get('community_id')
        
        if not latitude or not longitude:
            return Response({'error': 'latitude y longitude son requeridos'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener API key desde settings
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        if not api_key:
            # Datos simulados si no hay API key
            weather_data = self._create_simulated_weather(latitude, longitude, community_id)
            serializer = self.get_serializer(weather_data)
            return Response(serializer.data)
        
        # Llamar a OpenWeatherMap API
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': api_key,
                'units': 'metric',
                'lang': 'es'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Crear registro en BD
            weather_data = WeatherData.objects.create(
                community_id=community_id,
                latitude=latitude,
                longitude=longitude,
                date=datetime.now().date(),
                time=datetime.now().time(),
                temperature=data['main']['temp'],
                feels_like=data['main'].get('feels_like'),
                temp_min=data['main'].get('temp_min'),
                temp_max=data['main'].get('temp_max'),
                humidity=data['main']['humidity'],
                pressure=data['main'].get('pressure'),
                wind_speed=data['wind'].get('speed'),
                wind_direction=data['wind'].get('deg'),
                weather_condition=data['weather'][0]['main'],
                weather_description=data['weather'][0]['description'],
                cloudiness=data['clouds'].get('all'),
                visibility=data.get('visibility'),
                data_source='OpenWeatherMap'
            )
            
            serializer = self.get_serializer(weather_data)
            return Response(serializer.data)
            
        except requests.RequestException as e:
            return Response({'error': f'Error al obtener datos climáticos: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _create_simulated_weather(self, latitude, longitude, community_id):
        """Crear datos climáticos simulados"""
        import random
        
        weather_data = WeatherData.objects.create(
            community_id=community_id,
            latitude=latitude,
            longitude=longitude,
            date=datetime.now().date(),
            time=datetime.now().time(),
            temperature=round(random.uniform(15, 30), 2),
            feels_like=round(random.uniform(15, 30), 2),
            temp_min=round(random.uniform(10, 20), 2),
            temp_max=round(random.uniform(25, 35), 2),
            humidity=round(random.uniform(40, 90), 2),
            pressure=round(random.uniform(1000, 1020), 2),
            wind_speed=round(random.uniform(0, 15), 2),
            wind_direction=random.randint(0, 360),
            precipitation=round(random.uniform(0, 5), 2),
            weather_condition='Clear',
            weather_description='Cielo despejado',
            cloudiness=random.randint(0, 50),
            visibility=10000,
            uv_index=round(random.uniform(0, 11), 2),
            data_source='Simulado'
        )
        return weather_data

    @action(detail=False, methods=['get'])
    def by_community(self, request):
        """Obtener datos climáticos por comunidad"""
        community_id = request.query_params.get('community_id')
        days = int(request.query_params.get('days', 7))
        
        if not community_id:
            return Response({'error': 'community_id es requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        from_date = datetime.now().date() - timedelta(days=days)
        weather_data = self.queryset.filter(
            community_id=community_id,
            date__gte=from_date
        )
        
        serializer = self.get_serializer(weather_data, many=True)
        return Response(serializer.data)


class WeatherForecastViewSet(viewsets.ModelViewSet):
    """ViewSet para pronósticos del tiempo"""
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['community', 'forecast_date']
    ordering_fields = ['forecast_date']
    ordering = ['forecast_date']

    @action(detail=False, methods=['post'])
    def fetch_forecast(self, request):
        """Obtener pronóstico desde API"""
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        community_id = request.data.get('community_id')
        
        if not latitude or not longitude:
            return Response({'error': 'latitude y longitude son requeridos'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        if not api_key:
            # Crear pronóstico simulado
            forecasts = self._create_simulated_forecast(latitude, longitude, community_id)
            serializer = self.get_serializer(forecasts, many=True)
            return Response(serializer.data)
        
        # Llamar a API real
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': api_key,
                'units': 'metric',
                'lang': 'es'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data['list'][:8]:  # Próximos 8 registros (24 horas)
                forecast_dt = datetime.fromtimestamp(item['dt'])
                forecast = WeatherForecast.objects.create(
                    community_id=community_id,
                    latitude=latitude,
                    longitude=longitude,
                    forecast_date=forecast_dt.date(),
                    forecast_time=forecast_dt.time(),
                    temperature=item['main']['temp'],
                    temp_min=item['main']['temp_min'],
                    temp_max=item['main']['temp_max'],
                    weather_condition=item['weather'][0]['main'],
                    precipitation_probability=item.get('pop', 0) * 100,
                    precipitation_amount=item.get('rain', {}).get('3h', 0),
                    wind_speed=item['wind'].get('speed'),
                    humidity=item['main']['humidity'],
                    data_source='OpenWeatherMap'
                )
                forecasts.append(forecast)
            
            serializer = self.get_serializer(forecasts, many=True)
            return Response(serializer.data)
            
        except requests.RequestException as e:
            return Response({'error': f'Error al obtener pronóstico: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _create_simulated_forecast(self, latitude, longitude, community_id):
        """Crear pronóstico simulado para 5 días"""
        import random
        
        forecasts = []
        for i in range(5):
            forecast_date = datetime.now().date() + timedelta(days=i+1)
            forecast = WeatherForecast.objects.create(
                community_id=community_id,
                latitude=latitude,
                longitude=longitude,
                forecast_date=forecast_date,
                temperature=round(random.uniform(15, 30), 2),
                temp_min=round(random.uniform(10, 20), 2),
                temp_max=round(random.uniform(25, 35), 2),
                weather_condition=random.choice(['Clear', 'Clouds', 'Rain']),
                precipitation_probability=round(random.uniform(0, 100), 2),
                precipitation_amount=round(random.uniform(0, 10), 2),
                wind_speed=round(random.uniform(0, 15), 2),
                humidity=round(random.uniform(40, 90), 2),
                data_source='Simulado'
            )
            forecasts.append(forecast)
        
        return forecasts


class WeatherAlertViewSet(viewsets.ModelViewSet):
    """ViewSet para alertas climáticas"""
    queryset = WeatherAlert.objects.all()
    serializer_class = WeatherAlertSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['community', 'alert_type', 'severity', 'is_active']
    ordering_fields = ['created_at', 'start_date']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active_alerts(self, request):
        """Obtener alertas activas"""
        from django.utils import timezone
        now = timezone.now()
        
        active = self.queryset.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        )
        
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Desactivar una alerta"""
        alert = self.get_object()
        alert.is_active = False
        alert.save()
        
        serializer = self.get_serializer(alert)
        return Response(serializer.data)
