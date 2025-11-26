from django.db import models
from django.core.validators import RegexValidator
from users.models import User


class Community(models.Model):
    """Comunidades"""
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        db_table = 'communities'
        verbose_name = 'Comunidad'
        verbose_name_plural = 'Comunidades'
        ordering = ['name']

    def __str__(self):
        return self.name


class Partner(models.Model):
    """Socios de la cooperativa"""
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    SUSPENDED = 'SUSPENDED'
    
    STATUS_CHOICES = [
        (ACTIVE, 'Activo'),
        (INACTIVE, 'Inactivo'),
        (SUSPENDED, 'Suspendido'),
    ]
    
    ci_validator = RegexValidator(
        regex=r'^\d{7,10}$',
        message="El CI debe contener entre 7 y 10 dígitos."
    )
    
    nit_validator = RegexValidator(
        regex=r'^\d{7,15}$',
        message="El NIT debe contener entre 7 y 15 dígitos."
    )
    
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    
    # Información personal
    ci = models.CharField(max_length=10, unique=True, validators=[ci_validator], verbose_name='Cédula de Identidad')
    nit = models.CharField(max_length=15, unique=True, validators=[nit_validator], blank=True, null=True, verbose_name='NIT')
    first_name = models.CharField(max_length=100, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    
    # Información de contacto
    email = models.EmailField(blank=True, verbose_name='Correo electrónico')
    phone = models.CharField(max_length=17, validators=[phone_validator], verbose_name='Teléfono')
    address = models.TextField(blank=True, verbose_name='Dirección')
    
    # Relaciones
    community = models.ForeignKey(Community, on_delete=models.PROTECT, related_name='partners', verbose_name='Comunidad')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='partner', verbose_name='Usuario asociado')
    
    # Estado y metadatos
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE, verbose_name='Estado')
    registration_date = models.DateField(auto_now_add=True, verbose_name='Fecha de registro')
    notes = models.TextField(blank=True, verbose_name='Notas')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='created_partners', verbose_name='Creado por')

    class Meta:
        db_table = 'partners'
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ci']),
            models.Index(fields=['nit']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - CI: {self.ci}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def total_parcels(self):
        return self.parcels.count()

    @property
    def total_surface(self):
        return self.parcels.aggregate(models.Sum('surface'))['surface__sum'] or 0
