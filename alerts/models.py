from django.db import models
from tenants.managers import TenantModel
from users.models import User


class Alert(TenantModel):
    """Modelo para alertas del sistema"""
    
    ALERT_TYPES = [
        ('WEATHER', 'Clima Adverso'),
        ('PRICE', 'Precio de Mercado'),
        ('HARVEST', 'Momento de Cosecha'),
        ('FERTILIZATION', 'Fertilización'),
        ('PEST', 'Plagas/Enfermedades'),
    ]
    
    SEVERITY_LEVELS = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('CRITICAL', 'Crítica'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Datos adicionales en JSON
    data = models.JSONField(default=dict, blank=True)
    
    # Estado
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Destinatarios (si es None, es para toda la organización)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='alerts')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['alert_type', 'severity']),
            models.Index(fields=['is_active', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.title}"
