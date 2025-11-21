from django.contrib import admin
from .models import WeatherData, WeatherForecast, WeatherAlert


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['community', 'date', 'time', 'temperature', 'humidity', 
                    'weather_condition', 'data_source']
    list_filter = ['date', 'weather_condition', 'data_source', 'community']
    search_fields = ['community__name', 'weather_description']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Ubicación', {
            'fields': ('community', 'latitude', 'longitude')
        }),
        ('Fecha y Hora', {
            'fields': ('date', 'time')
        }),
        ('Temperatura', {
            'fields': ('temperature', 'feels_like', 'temp_min', 'temp_max')
        }),
        ('Condiciones', {
            'fields': ('weather_condition', 'weather_description', 'humidity', 'pressure')
        }),
        ('Viento', {
            'fields': ('wind_speed', 'wind_direction')
        }),
        ('Precipitación', {
            'fields': ('precipitation', 'rain_probability')
        }),
        ('Otros', {
            'fields': ('cloudiness', 'visibility', 'uv_index')
        }),
        ('Metadatos', {
            'fields': ('data_source', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ['community', 'forecast_date', 'forecast_time', 'temperature', 
                    'precipitation_probability', 'data_source']
    list_filter = ['forecast_date', 'weather_condition', 'data_source']
    search_fields = ['community__name']
    date_hierarchy = 'forecast_date'
    readonly_fields = ['created_at']


@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ['community', 'alert_type', 'severity', 'title', 'is_active', 
                    'start_date', 'end_date']
    list_filter = ['alert_type', 'severity', 'is_active', 'start_date']
    search_fields = ['title', 'description', 'community__name']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Alerta', {
            'fields': ('community', 'alert_type', 'severity', 'title', 'description')
        }),
        ('Vigencia', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Recomendaciones', {
            'fields': ('action_recommended',)
        }),
        ('Metadatos', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
