from django.db import models
from users.models import User


class AuditLog(models.Model):
    """Bitácora de auditoría del sistema"""
    LOGIN = 'LOGIN'
    LOGOUT = 'LOGOUT'
    LOGIN_FAILED = 'LOGIN_FAILED'
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    
    ACTION_CHOICES = [
        (LOGIN, 'Inicio de sesión'),
        (LOGOUT, 'Cierre de sesión'),
        (LOGIN_FAILED, 'Intento fallido de inicio de sesión'),
        (CREATE, 'Creación'),
        (UPDATE, 'Actualización'),
        (DELETE, 'Eliminación'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='audit_logs', verbose_name='Usuario')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='Acción')
    model_name = models.CharField(max_length=100, blank=True, verbose_name='Modelo')
    object_id = models.IntegerField(null=True, blank=True, verbose_name='ID del objeto')
    description = models.TextField(verbose_name='Descripción')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='Dirección IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')

    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['model_name', 'object_id']),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else 'Sistema'
        return f"{user_str} - {self.get_action_display()} - {self.timestamp}"
