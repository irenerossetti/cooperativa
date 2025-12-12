from django.db import models
from django.contrib.auth import get_user_model
from tenants.managers import TenantModel

User = get_user_model()


class Notification(TenantModel):
    """
    Modelo para notificaciones del sistema
    """
    TYPE_CHOICES = [
        ('INFO', 'Información'),
        ('SUCCESS', 'Éxito'),
        ('WARNING', 'Advertencia'),
        ('ERROR', 'Error'),
        ('SALE', 'Venta'),
        ('PAYMENT', 'Pago'),
        ('STOCK', 'Inventario'),
        ('REQUEST', 'Solicitud'),
        ('ALERT', 'Alerta'),
        ('TASK', 'Tarea'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Usuario'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    message = models.TextField(verbose_name='Mensaje')
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='INFO',
        verbose_name='Tipo'
    )
    read = models.BooleanField(default=False, verbose_name='Leída')
    
    # Datos adicionales en JSON
    extra_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Datos adicionales',
        help_text='Información adicional en formato JSON'
    )
    
    # URL de acción (opcional)
    action_url = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='URL de acción'
    )
    
    # Vinculación con alertas
    alert = models.ForeignKey(
        'alerts.Alert',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='Alerta relacionada'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de lectura')

    class Meta:
        db_table = 'notifications_notification'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'read', '-created_at']),
            models.Index(fields=['type', '-created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def mark_as_read(self):
        """Marca la notificación como leída"""
        if not self.read:
            self.read = True
            from django.utils import timezone
            self.read_at = timezone.now()
            self.save(update_fields=['read', 'read_at'])


class NotificationPreference(TenantModel):
    """
    Preferencias de notificación por usuario
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name='Usuario'
    )
    
    # Canales habilitados
    email_enabled = models.BooleanField(default=True, verbose_name='Email habilitado')
    push_enabled = models.BooleanField(default=True, verbose_name='Push habilitado')
    
    # Tipos de notificaciones habilitadas
    notify_sales = models.BooleanField(default=True, verbose_name='Notificar ventas')
    notify_payments = models.BooleanField(default=True, verbose_name='Notificar pagos')
    notify_stock = models.BooleanField(default=True, verbose_name='Notificar stock')
    notify_requests = models.BooleanField(default=True, verbose_name='Notificar solicitudes')
    notify_alerts = models.BooleanField(default=True, verbose_name='Notificar alertas')
    notify_tasks = models.BooleanField(default=True, verbose_name='Notificar tareas')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications_preference'
        verbose_name = 'Preferencia de notificación'
        verbose_name_plural = 'Preferencias de notificación'

    def __str__(self):
        return f"Preferencias de {self.user.username}"
