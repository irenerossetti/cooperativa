from django.contrib import admin
from .models import CropMonitoring, CropAlert


@admin.register(CropMonitoring)
class CropMonitoringAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'campaign', 'monitoring_date', 'phenological_stage', 
                    'health_status', 'pest_presence', 'disease_presence']
    list_filter = ['phenological_stage', 'health_status', 'monitoring_date', 
                   'pest_presence', 'disease_presence']
    search_fields = ['parcel__code', 'campaign__name', 'observations']
    date_hierarchy = 'monitoring_date'
    readonly_fields = ['recorded_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('parcel', 'campaign', 'monitoring_date')
        }),
        ('Estado del Cultivo', {
            'fields': ('phenological_stage', 'health_status')
        }),
        ('Métricas', {
            'fields': ('plant_height', 'leaf_color_index', 'soil_moisture', 'temperature')
        }),
        ('Incidencias', {
            'fields': ('pest_presence', 'pest_details', 'disease_presence', 'disease_details')
        }),
        ('Observaciones', {
            'fields': ('observations', 'recommendations', 'images')
        }),
        ('Metadatos', {
            'fields': ('recorded_by', 'recorded_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CropAlert)
class CropAlertAdmin(admin.ModelAdmin):
    list_display = ['monitoring', 'alert_type', 'severity', 'title', 'is_active', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Alerta', {
            'fields': ('monitoring', 'alert_type', 'severity', 'title', 'description')
        }),
        ('Estado', {
            'fields': ('is_active', 'resolved_at', 'resolution_notes')
        }),
        ('Metadatos', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
