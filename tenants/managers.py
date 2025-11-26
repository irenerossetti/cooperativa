from django.db import models
from .middleware import get_current_organization


class TenantManager(models.Manager):
    """
    Manager que filtra automáticamente por la organización actual.
    """
    
    def get_queryset(self):
        queryset = super().get_queryset()
        organization = get_current_organization()
        
        if organization:
            return queryset.filter(organization=organization)
        
        return queryset
    
    def all_organizations(self):
        """Método para obtener registros de todas las organizaciones (sin filtro)"""
        return super().get_queryset()


class TenantModel(models.Model):
    """
    Modelo base abstracto para modelos que pertenecen a una organización.
    """
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Organización',
        db_index=True
    )
    
    objects = TenantManager()
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        # Auto-asignar la organización actual si no está establecida
        if not self.organization_id:
            organization = get_current_organization()
            if organization:
                self.organization = organization
            else:
                raise ValueError(
                    f'No se puede guardar {self.__class__.__name__} sin una organización. '
                    'Asegúrate de que el middleware TenantMiddleware esté configurado.'
                )
        super().save(*args, **kwargs)
