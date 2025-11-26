from django.db import models
from partners.models import Partner, Community
from parcels.models import Parcel
from campaigns.models import Campaign
from users.models import User
from tenants.managers import TenantModel


class ReportType(TenantModel):
    """Tipos de reportes"""
    PERFORMANCE = 'PERFORMANCE'
    FINANCIAL = 'FINANCIAL'
    POPULATION = 'POPULATION'
    HECTARES = 'HECTARES'
    TRACEABILITY = 'TRACEABILITY'
    CUSTOM = 'CUSTOM'
    
    TYPE_CHOICES = [
        (PERFORMANCE, 'Rendimiento'),
        (FINANCIAL, 'Financiero'),
        (POPULATION, 'Población'),
        (HECTARES, 'Hectáreas'),
        (TRACEABILITY, 'Trazabilidad'),
        (CUSTOM, 'Personalizado'),
    ]
    
    name = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'report_types'
        verbose_name = 'Tipo de Reporte'
        verbose_name_plural = 'Tipos de Reportes'

    class Meta:
        unique_together = [
            ['organization', 'name'],
        ]

    def __str__(self):
        return self.get_name_display()


class GeneratedReport(TenantModel):
    """Reportes generados"""
    PDF = 'PDF'
    EXCEL = 'EXCEL'
    CSV = 'CSV'
    
    FORMAT_CHOICES = [
        (PDF, 'PDF'),
        (EXCEL, 'Excel'),
        (CSV, 'CSV'),
    ]
    
    report_type = models.ForeignKey(ReportType, on_delete=models.PROTECT,
                                   related_name='generated_reports')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Filtros aplicados
    filters = models.JSONField(default=dict, verbose_name='Filtros aplicados')
    
    # Archivo
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.IntegerField(null=True, blank=True, verbose_name='Tamaño (bytes)')
    
    # Datos del reporte
    data = models.JSONField(default=dict, verbose_name='Datos del reporte')
    
    # Metadatos
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    related_name='generated_reports')
    
    # Acceso
    is_public = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'generated_reports'
        verbose_name = 'Reporte Generado'
        verbose_name_plural = 'Reportes Generados'
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.title} - {self.generated_at.strftime('%Y-%m-%d')}"
