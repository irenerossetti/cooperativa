from django.db import models
from production.models import HarvestedProduct


class PriceTrend(models.Model):
    """Tendencias de precios"""
    product_name = models.CharField(max_length=200)
    date = models.DateField()
    
    # Precios
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Volumen
    volume_traded = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Análisis
    trend_direction = models.CharField(max_length=20, choices=[
        ('UP', 'Subiendo'), ('DOWN', 'Bajando'), ('STABLE', 'Estable')
    ])
    volatility = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Metadatos
    data_source = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'price_trends'
        verbose_name = 'Tendencia de Precio'
        verbose_name_plural = 'Tendencias de Precios'
        ordering = ['-date']
        unique_together = ['product_name', 'date']

    def __str__(self):
        return f"{self.product_name} - {self.date} - {self.average_price}"


class DemandTrend(models.Model):
    """Tendencias de demanda"""
    product_name = models.CharField(max_length=200)
    date = models.DateField()
    
    # Demanda
    demand_level = models.CharField(max_length=20, choices=[
        ('HIGH', 'Alta'), ('MEDIUM', 'Media'), ('LOW', 'Baja')
    ])
    demand_index = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Análisis
    trend_direction = models.CharField(max_length=20, choices=[
        ('INCREASING', 'Aumentando'), ('STABLE', 'Estable'), ('DECREASING', 'Disminuyendo')
    ])
    
    # Factores
    seasonal_factor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    market_factors = models.JSONField(default=dict)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demand_trends'
        verbose_name = 'Tendencia de Demanda'
        verbose_name_plural = 'Tendencias de Demanda'
        ordering = ['-date']
        unique_together = ['product_name', 'date']

    def __str__(self):
        return f"{self.product_name} - {self.date} - {self.demand_level}"
