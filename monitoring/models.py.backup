from django.db import models
from parcels.models import Parcel
from campaigns.models import Campaign
from users.models import User


class CropMonitoring(models.Model):
    """Monitoreo de estado de cultivos"""
    SEEDLING = 'SEEDLING'
    VEGETATIVE = 'VEGETATIVE'
    FLOWERING = 'FLOWERING'
    FRUITING = 'FRUITING'
    RIPENING = 'RIPENING'
    HARVEST_READY = 'HARVEST_READY'
    
    PHENOLOGICAL_STAGES = [
        (SEEDLING, 'Plántula'),
        (VEGETATIVE, 'Vegetativo'),
        (FLOWERING, 'Floración'),
        (FRUITING, 'Fructificación'),
        (RIPENING, 'Maduración'),
        (HARVEST_READY, 'Listo para Cosecha'),
    ]
    
    EXCELLENT = 'EXCELLENT'
    GOOD = 'GOOD'
    FAIR = 'FAIR'
    POOR = 'POOR'
    CRITICAL = 'CRITICAL'
    
    HEALTH_STATUS = [
        (EXCELLENT, 'Excelente'),
        (GOOD, 'Bueno'),
        (FAIR, 'Regular'),
        (POOR, 'Malo'),
        (CRITICAL, 'Crítico'),
    ]
    
    # Relaciones
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE,
                               related_name='monitoring_records', verbose_name='Parcela')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE,
                                 related_name='monitoring_records', verbose_name='Campaña')
    
    # Estado fenológico
    phenological_stage = models.CharField(max_length=20, choices=PHENOLOGICAL_STAGES,
                                         verbose_name='Etapa fenológica')
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS,
                                    verbose_name='Estado de salud')
    
    # Métricas
    plant_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                      verbose_name='Altura de planta (cm)')
    leaf_color_index = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                          verbose_name='Índice de color de hoja')
    soil_moisture = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                       verbose_name='Humedad del suelo (%)')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                     verbose_name='Temperatura (°C)')
    
    # Incidencias
    pest_presence = models.BooleanField(default=False, verbose_name='Presencia de plagas')
    disease_presence = models.BooleanField(default=False, verbose_name='Presencia de enfermedades')
    pest_details = models.TextField(blank=True, verbose_name='Detalles de plagas')
    disease_details = models.TextField(blank=True, verbose_name='Detalles de enfermedades')
    
    # Observaciones
    observations = models.TextField(blank=True, verbose_name='Observaciones')
    recommendations = models.TextField(blank=True, verbose_name='Recomendaciones')
    
    # Imágenes (URLs o paths)
    images = models.JSONField(default=list, verbose_name='Imágenes')
    
    # Metadatos
    monitoring_date = models.DateField(verbose_name='Fecha de monitoreo')
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    related_name='monitoring_records', verbose_name='Registrado por')

    class Meta:
        db_table = 'crop_monitoring'
        verbose_name = 'Monitoreo de Cultivo'
        verbose_name_plural = 'Monitoreos de Cultivos'
        ordering = ['-monitoring_date']
        indexes = [
            models.Index(fields=['parcel', 'monitoring_date']),
            models.Index(fields=['campaign', 'health_status']),
        ]

    def __str__(self):
        return f"{self.parcel.code} - {self.monitoring_date} - {self.get_health_status_display()}"


class CropAlert(models.Model):
    """Alertas de cultivos"""
    PEST = 'PEST'
    DISEASE = 'DISEASE'
    WATER_STRESS = 'WATER_STRESS'
    NUTRIENT_DEFICIENCY = 'NUTRIENT_DEFICIENCY'
    WEATHER = 'WEATHER'
    OTHER = 'OTHER'
    
    ALERT_TYPES = [
        (PEST, 'Plaga'),
        (DISEASE, 'Enfermedad'),
        (WATER_STRESS, 'Estrés Hídrico'),
        (NUTRIENT_DEFICIENCY, 'Deficiencia Nutricional'),
        (WEATHER, 'Clima'),
        (OTHER, 'Otro'),
    ]
    
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'
    
    SEVERITY_LEVELS = [
        (LOW, 'Baja'),
        (MEDIUM, 'Media'),
        (HIGH, 'Alta'),
        (CRITICAL, 'Crítica'),
    ]
    
    # Relaciones
    monitoring = models.ForeignKey(CropMonitoring, on_delete=models.CASCADE,
                                  related_name='alerts', verbose_name='Monitoreo')
    
    # Alerta
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES, verbose_name='Tipo de alerta')
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, verbose_name='Severidad')
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='Resuelta el')
    resolution_notes = models.TextField(blank=True, verbose_name='Notas de resolución')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'crop_alerts'
        verbose_name = 'Alerta de Cultivo'
        verbose_name_plural = 'Alertas de Cultivos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.get_severity_display()}"
