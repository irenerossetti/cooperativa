from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator


class Organization(models.Model):
    """
    Modelo para multi-tenancy. Cada cooperativa es una organización.
    """
    PLAN_CHOICES = [
        ('FREE', 'Gratuito'),
        ('BASIC', 'Básico'),
        ('PROFESSIONAL', 'Profesional'),
        ('ENTERPRISE', 'Enterprise'),
    ]
    
    STATUS_CHOICES = [
        ('TRIAL', 'Prueba'),
        ('ACTIVE', 'Activo'),
        ('SUSPENDED', 'Suspendido'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    # Información básica
    name = models.CharField('Nombre', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True, db_index=True)
    subdomain = models.CharField(
        'Subdominio',
        max_length=63,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$',
                message='El subdominio solo puede contener letras minúsculas, números y guiones.'
            )
        ],
        help_text='Subdominio único para acceder: subdominio.tuapp.com'
    )
    
    # Información de contacto
    email = models.EmailField('Email de contacto')
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    address = models.TextField('Dirección', blank=True)
    
    # Plan y estado
    plan = models.CharField('Plan', max_length=20, choices=PLAN_CHOICES, default='FREE')
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default='TRIAL')
    
    # Límites según el plan
    max_users = models.IntegerField('Máximo de usuarios', default=5)
    max_products = models.IntegerField('Máximo de productos', default=100)
    max_storage_mb = models.IntegerField('Almacenamiento (MB)', default=100)
    
    # Fechas
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    trial_ends_at = models.DateTimeField('Fin de prueba', null=True, blank=True)
    subscription_ends_at = models.DateTimeField('Fin de suscripción', null=True, blank=True)
    
    # Configuración
    is_active = models.BooleanField('Activo', default=True)
    settings = models.JSONField('Configuración', default=dict, blank=True)
    
    class Meta:
        db_table = 'tenants_organization'
        verbose_name = 'Organización'
        verbose_name_plural = 'Organizaciones'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.subdomain:
            self.subdomain = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def is_trial(self):
        return self.status == 'TRIAL'
    
    @property
    def is_subscription_active(self):
        return self.status == 'ACTIVE'
    
    def get_plan_display_name(self):
        return dict(self.PLAN_CHOICES).get(self.plan, self.plan)


class OrganizationMember(models.Model):
    """
    Relación entre usuarios y organizaciones.
    Un usuario puede pertenecer a múltiples organizaciones.
    """
    ROLE_CHOICES = [
        ('OWNER', 'Propietario'),
        ('ADMIN', 'Administrador'),
        ('MEMBER', 'Miembro'),
    ]
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='Organización'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='organization_memberships',
        verbose_name='Usuario'
    )
    role = models.CharField('Rol', max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    is_active = models.BooleanField('Activo', default=True)
    joined_at = models.DateTimeField('Fecha de ingreso', auto_now_add=True)
    
    class Meta:
        db_table = 'tenants_organization_member'
        verbose_name = 'Miembro de Organización'
        verbose_name_plural = 'Miembros de Organizaciones'
        unique_together = [['organization', 'user']]
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role})"
