from django.db import models
from parcels.models import Parcel
from partners.models import Community


class WeatherData(models.Model):
    """Datos climáticos"""
    # Ubicación
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='weather_data', verbose_name='Comunidad')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name='Latitud')
    longitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name='Longitud')
    
    # Fecha y hora
    date = models.DateField(verbose_name='Fecha')
    time = models.TimeField(null=True, blank=True, verbose_name='Hora')
    
    # Temperatura
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Temperatura (°C)')
    feels_like = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                     verbose_name='Sensación térmica (°C)')
    temp_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                   verbose_name='Temperatura mínima (°C)')
    temp_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                   verbose_name='Temperatura máxima (°C)')
    
    # Humedad y presión
    humidity = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Humedad (%)')
    pressure = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True,
                                  verbose_name='Presión (hPa)')
    
    # Viento
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                    verbose_name='Velocidad del viento (m/s)')
    wind_direction = models.IntegerField(null=True, blank=True, verbose_name='Dirección del viento (°)')
    
    # Precipitación
    precipitation = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                       verbose_name='Precipitación (mm)')
    rain_probability = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                          verbose_name='Probabilidad de lluvia (%)')
    
    # Condiciones
    weather_condition = models.CharField(max_length=100, blank=True, verbose_name='Condición climática')
    weather_description = models.CharField(max_length=200, blank=True, verbose_name='Descripción')
    
    # Nubosidad y visibilidad
    cloudiness = models.IntegerField(null=True, blank=True, verbose_name='Nubosidad (%)')
    visibility = models.IntegerField(null=True, blank=True, verbose_name='Visibilidad (m)')
    
    # UV Index
    uv_index = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                  verbose_name='Índice UV')
    
    # Fuente de datos
    data_source = models.CharField(max_length=100, default='OpenWeatherMap', verbose_name='Fuente')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        db_table = 'weather_data'
        verbose_name = 'Dato Climático'
        verbose_name_plural = 'Datos Climáticos'
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['community', 'date']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.community.name if self.community else 'General'} - {self.date} - {self.temperature}°C"


class WeatherForecast(models.Model):
    """Pronóstico del tiempo"""
    # Ubicación
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='weather_forecasts', verbose_name='Comunidad')
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    # Pronóstico
    forecast_date = models.DateField(verbose_name='Fecha del pronóstico')
    forecast_time = models.TimeField(null=True, blank=True, verbose_name='Hora')
    
    # Temperatura
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    temp_min = models.DecimalField(max_digits=5, decimal_places=2)
    temp_max = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Condiciones
    weather_condition = models.CharField(max_length=100)
    precipitation_probability = models.DecimalField(max_digits=5, decimal_places=2,
                                                   verbose_name='Probabilidad de lluvia (%)')
    precipitation_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                              verbose_name='Cantidad de lluvia (mm)')
    
    # Viento
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Humedad
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Fuente
    data_source = models.CharField(max_length=100, default='OpenWeatherMap')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'weather_forecasts'
        verbose_name = 'Pronóstico del Tiempo'
        verbose_name_plural = 'Pronósticos del Tiempo'
        ordering = ['forecast_date', 'forecast_time']

    def __str__(self):
        return f"Pronóstico: {self.forecast_date} - {self.temperature}°C"


class WeatherAlert(models.Model):
    """Alertas climáticas tempranas"""
    FROST = 'FROST'
    HEAVY_RAIN = 'HEAVY_RAIN'
    DROUGHT = 'DROUGHT'
    STRONG_WIND = 'STRONG_WIND'
    HAIL = 'HAIL'
    EXTREME_HEAT = 'EXTREME_HEAT'
    
    ALERT_TYPES = [
        (FROST, 'Helada'),
        (HEAVY_RAIN, 'Lluvia Intensa'),
        (DROUGHT, 'Sequía'),
        (STRONG_WIND, 'Viento Fuerte'),
        (HAIL, 'Granizo'),
        (EXTREME_HEAT, 'Calor Extremo'),
    ]
    
    WARNING = 'WARNING'
    WATCH = 'WATCH'
    ADVISORY = 'ADVISORY'
    
    SEVERITY_LEVELS = [
        (WARNING, 'Advertencia'),
        (WATCH, 'Vigilancia'),
        (ADVISORY, 'Aviso'),
    ]
    
    # Ubicación
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='weather_alerts')
    
    # Alerta
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Vigencia
    start_date = models.DateTimeField(verbose_name='Inicio')
    end_date = models.DateTimeField(verbose_name='Fin')
    
    # Recomendaciones
    action_recommended = models.TextField(verbose_name='Acción recomendada')
    
    # Estado
    is_active = models.BooleanField(default=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'weather_alerts'
        verbose_name = 'Alerta Climática'
        verbose_name_plural = 'Alertas Climáticas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.get_severity_display()}"
