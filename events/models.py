from django.db import models
from django.contrib.auth import get_user_model
from tenants.managers import TenantModel

User = get_user_model()


class Event(TenantModel):
    """
    Eventos del calendario agrícola
    """
    TYPE_CHOICES = [
        ('SIEMBRA', 'Siembra'),
        ('COSECHA', 'Cosecha'),
        ('CAPACITACION', 'Capacitación'),
        ('REUNION', 'Reunión'),
        ('INSPECCION', 'Inspección'),
        ('MANTENIMIENTO', 'Mantenimiento'),
        ('APLICACION', 'Aplicación de Insumos'),
        ('OTRO', 'Otro'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('URGENT', 'Urgente'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Título')
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Tipo'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    
    # Fechas
    start_datetime = models.DateTimeField(verbose_name='Fecha y hora de inicio')
    end_datetime = models.DateTimeField(verbose_name='Fecha y hora de fin')
    all_day = models.BooleanField(default=False, verbose_name='Todo el día')
    
    # Ubicación
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ubicación'
    )
    
    # Relaciones
    parcels = models.ManyToManyField(
        'parcels.Parcel',
        blank=True,
        related_name='events',
        verbose_name='Parcelas'
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name='events',
        verbose_name='Participantes'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events',
        verbose_name='Creado por'
    )
    
    # Prioridad y estado
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name='Prioridad'
    )
    completed = models.BooleanField(default=False, verbose_name='Completado')
    
    # Recordatorios
    reminder_sent = models.BooleanField(
        default=False,
        verbose_name='Recordatorio enviado'
    )
    reminder_minutes = models.IntegerField(
        default=60,
        verbose_name='Minutos antes del recordatorio'
    )
    
    # Color para el calendario
    color = models.CharField(
        max_length=7,
        default='#3b82f6',
        verbose_name='Color',
        help_text='Color en formato hexadecimal (ej: #3b82f6)'
    )
    
    # Notas adicionales
    notes = models.TextField(blank=True, verbose_name='Notas')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events_event'
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['start_datetime']
        indexes = [
            models.Index(fields=['start_datetime', 'end_datetime']),
            models.Index(fields=['type', 'start_datetime']),
        ]

    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%d/%m/%Y')}"

    @property
    def duration_hours(self):
        """Calcula la duración del evento en horas"""
        delta = self.end_datetime - self.start_datetime
        return delta.total_seconds() / 3600

    @property
    def is_upcoming(self):
        """Verifica si el evento es próximo"""
        from django.utils import timezone
        return self.start_datetime > timezone.now()

    @property
    def is_past(self):
        """Verifica si el evento ya pasó"""
        from django.utils import timezone
        return self.end_datetime < timezone.now()


class EventReminder(models.Model):
    """
    Recordatorios de eventos
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='reminders',
        verbose_name='Evento'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuario'
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Enviado en'
    )
    method = models.CharField(
        max_length=20,
        choices=[
            ('EMAIL', 'Email'),
            ('NOTIFICATION', 'Notificación'),
            ('SMS', 'SMS'),
        ],
        default='NOTIFICATION',
        verbose_name='Método'
    )

    class Meta:
        db_table = 'events_reminder'
        verbose_name = 'Recordatorio'
        verbose_name_plural = 'Recordatorios'
        ordering = ['-sent_at']

    def __str__(self):
        return f"Recordatorio: {self.event.title} - {self.user.username}"
