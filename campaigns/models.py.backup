from django.db import models
from partners.models import Partner
from parcels.models import Parcel
from users.models import User


class Campaign(models.Model):
    """Campañas agrícolas"""
    PLANNING = 'PLANNING'
    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    
    STATUS_CHOICES = [
        (PLANNING, 'En Planificación'),
        (ACTIVE, 'Activa'),
        (COMPLETED, 'Completada'),
        (CANCELLED, 'Cancelada'),
    ]
    
    # Información básica
    code = models.CharField(max_length=50, unique=True, verbose_name='Código de campaña')
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    
    # Fechas
    start_date = models.DateField(verbose_name='Fecha de inicio')
    end_date = models.DateField(verbose_name='Fecha de fin estimada')
    actual_end_date = models.DateField(null=True, blank=True, verbose_name='Fecha de fin real')
    
    # Metas
    target_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Área objetivo (ha)')
    target_production = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, 
                                           verbose_name='Producción objetivo (kg)')
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PLANNING, verbose_name='Estado')
    
    # Relaciones
    partners = models.ManyToManyField(Partner, related_name='campaigns', verbose_name='Socios participantes')
    parcels = models.ManyToManyField(Parcel, related_name='campaigns', verbose_name='Parcelas asignadas')
    
    # Metadatos
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='created_campaigns', verbose_name='Creado por')

    class Meta:
        db_table = 'campaigns'
        verbose_name = 'Campaña'
        verbose_name_plural = 'Campañas'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def total_area(self):
        """Área total de parcelas asignadas"""
        return self.parcels.aggregate(models.Sum('surface'))['surface__sum'] or 0

    @property
    def total_partners(self):
        """Total de socios participantes"""
        return self.partners.count()

    @property
    def is_active(self):
        """Verifica si la campaña está activa"""
        return self.status == self.ACTIVE
