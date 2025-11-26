from django.db import models
from campaigns.models import Campaign
from parcels.models import Parcel
from partners.models import Partner
from users.models import User


class HarvestedProduct(models.Model):
    """Productos cosechados"""
    # Información básica
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE,
                                 related_name='harvested_products', verbose_name='Campaña')
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE,
                               related_name='harvested_products', verbose_name='Parcela')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE,
                                related_name='harvested_products', verbose_name='Socio')
    
    # Detalles del producto
    product_name = models.CharField(max_length=200, verbose_name='Nombre del producto')
    harvest_date = models.DateField(verbose_name='Fecha de cosecha')
    
    # Cantidades
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad (kg)')
    quality_grade = models.CharField(max_length=50, blank=True, verbose_name='Grado de calidad')
    
    # Condiciones
    moisture_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                             verbose_name='Porcentaje de humedad')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                     verbose_name='Temperatura (°C)')
    
    # Almacenamiento
    storage_location = models.CharField(max_length=200, blank=True, verbose_name='Ubicación de almacenamiento')
    
    # Observaciones
    observations = models.TextField(blank=True, verbose_name='Observaciones')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='created_products', verbose_name='Creado por')

    class Meta:
        db_table = 'harvested_products'
        verbose_name = 'Producto Cosechado'
        verbose_name_plural = 'Productos Cosechados'
        ordering = ['-harvest_date']
        indexes = [
            models.Index(fields=['campaign', 'harvest_date']),
            models.Index(fields=['parcel']),
            models.Index(fields=['partner']),
        ]

    def __str__(self):
        return f"{self.product_name} - {self.parcel.code} ({self.harvest_date})"

    @property
    def yield_per_hectare(self):
        """Rendimiento por hectárea"""
        if self.parcel.surface > 0:
            return self.quantity / self.parcel.surface
        return 0
