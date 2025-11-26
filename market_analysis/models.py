from django.db import models
from tenants.managers import TenantModel


class MarketPrice(TenantModel):
    """Modelo para almacenar precios de mercado de productos agrícolas"""
    
    PRODUCT_TYPES = [
        ('QUINUA', 'Quinua'),
        ('PAPA', 'Papa'),
        ('MAIZ', 'Maíz'),
        ('TRIGO', 'Trigo'),
        ('CEBADA', 'Cebada'),
        ('HABA', 'Haba'),
        ('ARVEJA', 'Arveja'),
    ]
    
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    source = models.CharField(max_length=200, default='Sistema Interno')
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Precio de Mercado'
        verbose_name_plural = 'Precios de Mercado'
    
    def __str__(self):
        return f"{self.product_type} - Bs. {self.price_per_kg} ({self.date})"


class PriceAlert(TenantModel):
    """Modelo para alertas de precio"""
    
    ALERT_TYPES = [
        ('HIGH', 'Precio Alto'),
        ('LOW', 'Precio Bajo'),
        ('OPPORTUNITY', 'Oportunidad'),
    ]
    
    product_type = models.CharField(max_length=50)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    percentage_change = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Alerta de Precio'
        verbose_name_plural = 'Alertas de Precio'
    
    def __str__(self):
        return f"{self.product_type} - {self.alert_type}"
