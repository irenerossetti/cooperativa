from django.db import models
from django.contrib.postgres.fields import JSONField
from partners.models import Partner
from parcels.models import Parcel, Crop
from campaigns.models import Campaign
from users.models import User
from tenants.managers import TenantModel


class AIRecommendationType(TenantModel):
    """Tipos de recomendaciones de IA"""
    PLANTING = 'PLANTING'
    FERTILIZATION = 'FERTILIZATION'
    HARVEST = 'HARVEST'
    MARKET = 'MARKET'
    PEST_CONTROL = 'PEST_CONTROL'
    
    TYPE_CHOICES = [
        (PLANTING, 'Recomendación de Siembra'),
        (FERTILIZATION, 'Plan de Fertilización'),
        (HARVEST, 'Momento Óptimo de Cosecha'),
        (MARKET, 'Oportunidad Comercial'),
        (PEST_CONTROL, 'Control de Plagas'),
    ]
    
    name = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Tipo')
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_recommendation_types'
        verbose_name = 'Tipo de Recomendación IA'
        verbose_name_plural = 'Tipos de Recomendaciones IA'

    class Meta:
        unique_together = [
            ['organization', 'name'],
        ]

    def __str__(self):
        return self.get_name_display()


class AIRecommendation(TenantModel):
    """Recomendaciones generadas por IA"""
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'
    
    PRIORITY_CHOICES = [
        (HIGH, 'Alta'),
        (MEDIUM, 'Media'),
        (LOW, 'Baja'),
    ]
    
    # Información básica
    recommendation_type = models.ForeignKey(AIRecommendationType, on_delete=models.PROTECT,
                                           related_name='recommendations', verbose_name='Tipo')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='ai_recommendations', verbose_name='Socio')
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='ai_recommendations', verbose_name='Parcela')
    
    # Recomendación
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=MEDIUM,
                               verbose_name='Prioridad')
    
    # Datos de IA
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                          verbose_name='Nivel de confianza (%)')
    ai_model_version = models.CharField(max_length=50, blank=True, verbose_name='Versión del modelo')
    input_data = models.JSONField(default=dict, verbose_name='Datos de entrada')
    output_data = models.JSONField(default=dict, verbose_name='Datos de salida')
    
    # Fechas
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de generación')
    valid_until = models.DateField(null=True, blank=True, verbose_name='Válido hasta')
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    was_applied = models.BooleanField(default=False, verbose_name='Fue aplicada')
    applied_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de aplicación')
    
    # Feedback
    user_rating = models.IntegerField(null=True, blank=True, verbose_name='Calificación (1-5)')
    user_feedback = models.TextField(blank=True, verbose_name='Comentarios del usuario')

    class Meta:
        db_table = 'ai_recommendations'
        verbose_name = 'Recomendación IA'
        verbose_name_plural = 'Recomendaciones IA'
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['partner', 'recommendation_type']),
            models.Index(fields=['parcel', 'is_active']),
        ]

    def __str__(self):
        return f"{self.title} - {self.partner.full_name if self.partner else 'General'}"


class PlantingRecommendation(TenantModel):
    """Recomendaciones específicas de siembra"""
    recommendation = models.OneToOneField(AIRecommendation, on_delete=models.CASCADE,
                                         related_name='planting_detail', verbose_name='Recomendación')
    
    # Cultivo recomendado
    recommended_crop = models.ForeignKey(Crop, on_delete=models.PROTECT,
                                        related_name='planting_recommendations',
                                        verbose_name='Cultivo recomendado')
    variety = models.CharField(max_length=200, blank=True, verbose_name='Variedad recomendada')
    
    # Fechas
    optimal_planting_date = models.DateField(verbose_name='Fecha óptima de siembra')
    planting_window_start = models.DateField(verbose_name='Inicio ventana de siembra')
    planting_window_end = models.DateField(verbose_name='Fin ventana de siembra')
    
    # Condiciones
    soil_conditions = models.JSONField(default=dict, verbose_name='Condiciones de suelo')
    climate_conditions = models.JSONField(default=dict, verbose_name='Condiciones climáticas')
    
    # Mercado
    market_demand = models.CharField(max_length=20, choices=[
        ('HIGH', 'Alta'), ('MEDIUM', 'Media'), ('LOW', 'Baja')
    ], verbose_name='Demanda de mercado')
    expected_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                        verbose_name='Precio esperado')
    
    # Estimaciones
    estimated_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         verbose_name='Rendimiento estimado (kg/ha)')
    estimated_harvest_date = models.DateField(null=True, blank=True,
                                             verbose_name='Fecha estimada de cosecha')

    class Meta:
        db_table = 'planting_recommendations'
        verbose_name = 'Detalle de Recomendación de Siembra'
        verbose_name_plural = 'Detalles de Recomendaciones de Siembra'

    def __str__(self):
        return f"Siembra: {self.recommended_crop.name} - {self.optimal_planting_date}"


class FertilizationPlan(TenantModel):
    """Planes de fertilización personalizados"""
    recommendation = models.OneToOneField(AIRecommendation, on_delete=models.CASCADE,
                                         related_name='fertilization_detail',
                                         verbose_name='Recomendación')
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE,
                               related_name='fertilization_plans', verbose_name='Parcela')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='fertilization_plans', verbose_name='Campaña')
    
    # Plan
    plan_name = models.CharField(max_length=200, verbose_name='Nombre del plan')
    start_date = models.DateField(verbose_name='Fecha de inicio')
    end_date = models.DateField(verbose_name='Fecha de fin')
    
    # Análisis de suelo
    soil_analysis = models.JSONField(default=dict, verbose_name='Análisis de suelo')
    nutrient_deficiencies = models.JSONField(default=list, verbose_name='Deficiencias nutricionales')
    
    # Objetivos
    target_yield = models.DecimalField(max_digits=10, decimal_places=2,
                                      verbose_name='Rendimiento objetivo (kg/ha)')
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'fertilization_plans'
        verbose_name = 'Plan de Fertilización'
        verbose_name_plural = 'Planes de Fertilización'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.plan_name} - {self.parcel.code}"


class FertilizationApplication(TenantModel):
    """Aplicaciones de fertilización dentro de un plan"""
    plan = models.ForeignKey(FertilizationPlan, on_delete=models.CASCADE,
                            related_name='applications', verbose_name='Plan')
    
    # Aplicación
    application_number = models.IntegerField(verbose_name='Número de aplicación')
    scheduled_date = models.DateField(verbose_name='Fecha programada')
    actual_date = models.DateField(null=True, blank=True, verbose_name='Fecha real')
    
    # Fertilizante
    fertilizer_type = models.CharField(max_length=200, verbose_name='Tipo de fertilizante')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad (kg)')
    application_method = models.CharField(max_length=100, verbose_name='Método de aplicación')
    
    # Nutrientes
    nutrients = models.JSONField(default=dict, verbose_name='Nutrientes (N-P-K)')
    
    # Estado
    is_completed = models.BooleanField(default=False, verbose_name='Completada')
    notes = models.TextField(blank=True, verbose_name='Notas')

    class Meta:
        db_table = 'fertilization_applications'
        verbose_name = 'Aplicación de Fertilización'
        verbose_name_plural = 'Aplicaciones de Fertilización'
        ordering = ['plan', 'application_number']

    def __str__(self):
        return f"{self.plan.plan_name} - Aplicación #{self.application_number}"


class HarvestRecommendation(TenantModel):
    """Recomendaciones de momento óptimo de cosecha"""
    recommendation = models.OneToOneField(AIRecommendation, on_delete=models.CASCADE,
                                         related_name='harvest_detail', verbose_name='Recomendación')
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE,
                               related_name='harvest_recommendations', verbose_name='Parcela')
    
    # Fechas
    optimal_harvest_date = models.DateField(verbose_name='Fecha óptima de cosecha')
    harvest_window_start = models.DateField(verbose_name='Inicio ventana de cosecha')
    harvest_window_end = models.DateField(verbose_name='Fin ventana de cosecha')
    
    # Factores
    maturity_level = models.DecimalField(max_digits=5, decimal_places=2,
                                        verbose_name='Nivel de maduración (%)')
    weather_conditions = models.JSONField(default=dict, verbose_name='Condiciones climáticas')
    market_conditions = models.JSONField(default=dict, verbose_name='Condiciones de mercado')
    
    # Logística
    logistics_readiness = models.CharField(max_length=20, choices=[
        ('READY', 'Listo'), ('PENDING', 'Pendiente'), ('NOT_READY', 'No listo')
    ], verbose_name='Estado logístico')
    storage_availability = models.BooleanField(default=True, verbose_name='Almacenamiento disponible')
    
    # Estimaciones
    estimated_yield = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name='Rendimiento estimado (kg)')
    estimated_quality = models.CharField(max_length=20, choices=[
        ('PREMIUM', 'Premium'), ('STANDARD', 'Estándar'), ('BASIC', 'Básico')
    ], verbose_name='Calidad estimada')

    class Meta:
        db_table = 'harvest_recommendations'
        verbose_name = 'Recomendación de Cosecha'
        verbose_name_plural = 'Recomendaciones de Cosecha'

    def __str__(self):
        return f"Cosecha: {self.parcel.code} - {self.optimal_harvest_date}"


class MarketOpportunity(TenantModel):
    """Oportunidades comerciales y tendencias de precios"""
    recommendation = models.OneToOneField(AIRecommendation, on_delete=models.CASCADE,
                                         related_name='market_detail', verbose_name='Recomendación')
    
    # Producto
    product_name = models.CharField(max_length=200, verbose_name='Producto')
    
    # Tendencias
    current_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio actual')
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name='Precio predicho')
    price_trend = models.CharField(max_length=20, choices=[
        ('RISING', 'Subiendo'), ('STABLE', 'Estable'), ('FALLING', 'Bajando')
    ], verbose_name='Tendencia de precio')
    
    # Demanda
    demand_level = models.CharField(max_length=20, choices=[
        ('HIGH', 'Alta'), ('MEDIUM', 'Media'), ('LOW', 'Baja')
    ], verbose_name='Nivel de demanda')
    demand_trend = models.CharField(max_length=20, choices=[
        ('INCREASING', 'Aumentando'), ('STABLE', 'Estable'), ('DECREASING', 'Disminuyendo')
    ], verbose_name='Tendencia de demanda')
    
    # Análisis
    market_analysis = models.JSONField(default=dict, verbose_name='Análisis de mercado')
    competitors_data = models.JSONField(default=dict, verbose_name='Datos de competidores')
    
    # Recomendación
    action_recommended = models.CharField(max_length=20, choices=[
        ('SELL_NOW', 'Vender Ahora'),
        ('WAIT', 'Esperar'),
        ('STORE', 'Almacenar'),
        ('PROCESS', 'Procesar')
    ], verbose_name='Acción recomendada')
    
    # Vigencia
    valid_from = models.DateField(verbose_name='Válido desde')
    valid_until = models.DateField(verbose_name='Válido hasta')

    class Meta:
        db_table = 'market_opportunities'
        verbose_name = 'Oportunidad de Mercado'
        verbose_name_plural = 'Oportunidades de Mercado'
        ordering = ['-valid_from']

    def __str__(self):
        return f"{self.product_name} - {self.get_action_recommended_display()}"


class AILearningData(TenantModel):
    """Datos de aprendizaje continuo de la IA"""
    recommendation = models.ForeignKey(AIRecommendation, on_delete=models.CASCADE,
                                      related_name='learning_data', verbose_name='Recomendación')
    
    # Resultado
    actual_outcome = models.JSONField(default=dict, verbose_name='Resultado real')
    predicted_outcome = models.JSONField(default=dict, verbose_name='Resultado predicho')
    
    # Métricas
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                        verbose_name='Precisión (%)')
    error_margin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                      verbose_name='Margen de error')
    
    # Feedback
    user_satisfaction = models.IntegerField(null=True, blank=True, verbose_name='Satisfacción (1-5)')
    was_successful = models.BooleanField(null=True, blank=True, verbose_name='Fue exitosa')
    
    # Metadatos
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    notes = models.TextField(blank=True, verbose_name='Notas')

    class Meta:
        db_table = 'ai_learning_data'
        verbose_name = 'Dato de Aprendizaje IA'
        verbose_name_plural = 'Datos de Aprendizaje IA'
        ordering = ['-recorded_at']

    def __str__(self):
        return f"Aprendizaje: {self.recommendation.title}"
