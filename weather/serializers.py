from rest_framework import serializers
from .models import WeatherData, WeatherForecast, WeatherAlert


class WeatherDataSerializer(serializers.ModelSerializer):
    community_name = serializers.CharField(source='community.name', read_only=True)
    
    class Meta:
        model = WeatherData
        fields = ['id', 'community', 'community_name', 'latitude', 'longitude', 'date', 'time',
                  'temperature', 'feels_like', 'temp_min', 'temp_max', 'humidity', 'pressure',
                  'wind_speed', 'wind_direction', 'precipitation', 'rain_probability',
                  'weather_condition', 'weather_description', 'cloudiness', 'visibility',
                  'uv_index', 'data_source', 'created_at']
        read_only_fields = ['created_at']


class WeatherForecastSerializer(serializers.ModelSerializer):
    community_name = serializers.CharField(source='community.name', read_only=True)
    
    class Meta:
        model = WeatherForecast
        fields = ['id', 'community', 'community_name', 'latitude', 'longitude',
                  'forecast_date', 'forecast_time', 'temperature', 'temp_min', 'temp_max',
                  'weather_condition', 'precipitation_probability', 'precipitation_amount',
                  'wind_speed', 'humidity', 'data_source', 'created_at']
        read_only_fields = ['created_at']


class WeatherAlertSerializer(serializers.ModelSerializer):
    community_name = serializers.CharField(source='community.name', read_only=True)
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = WeatherAlert
        fields = ['id', 'community', 'community_name', 'alert_type', 'alert_type_display',
                  'severity', 'severity_display', 'title', 'description', 'start_date',
                  'end_date', 'action_recommended', 'is_active', 'created_at']
        read_only_fields = ['created_at']
