from django.db import models
from parcels.models import Parcel
from campaigns.models import Campaign
from farm_activities.models import FarmActivity
from inventory.models import InventoryItem, InventoryMovement
from production.models import HarvestedProduct
from users.models import User


class ParcelTraceability(models.Model):
    """Trazabilidad completa de parcelas"""
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE,
                               related_name='traceability_records')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE,
                                 related_name='traceability_records')
    
    # Información general
    traceability_code = models.CharField(max_length=100, unique=True,
                                        verbose_name='Código de trazabilidad')
    start_date = models.DateField(verbose_name='Fecha de inicio')
    end_date = models.DateField(null=True, blank=True, verbose_name='Fecha de fin')
    
    # Resumen
    total_activities = models.IntegerField(default=0)
    total_inputs_used = models.IntegerField(default=0)
    total_production = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Estado
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'parcel_traceability'
        verbose_name = 'Trazabilidad de Parcela'
        verbose_name_plural = 'Trazabilidad de Parcelas'
        unique_together = ['parcel', 'campaign']

    def __str__(self):
        return f"{self.traceability_code} - {self.parcel.code}"


class InputUsageRecord(models.Model):
    """Registro de uso de insumos en parcelas"""
    traceability = models.ForeignKey(ParcelTraceability, on_delete=models.CASCADE,
                                    related_name='input_records')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT)
    farm_activity = models.ForeignKey(FarmActivity, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Uso
    application_date = models.DateField()
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2)
    application_method = models.CharField(max_length=200, blank=True)
    
    # Detalles
    purpose = models.CharField(max_length=200)
    weather_conditions = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    
    # Metadatos
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'input_usage_records'
        verbose_name = 'Registro de Uso de Insumo'
        verbose_name_plural = 'Registros de Uso de Insumos'
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.inventory_item.name} - {self.application_date}"
