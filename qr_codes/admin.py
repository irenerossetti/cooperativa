from django.contrib import admin
from .models import QRCode


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'model_type', 'object_id', 'scans_count', 'last_scanned_at', 'created_at']
    list_filter = ['model_type', 'created_at']
    search_fields = ['object_id', 'qr_data']
    readonly_fields = ['scans_count', 'last_scanned_at', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('model_type', 'object_id', 'qr_data')
        }),
        ('Imagen', {
            'fields': ('qr_image',)
        }),
        ('Estadísticas', {
            'fields': ('scans_count', 'last_scanned_at')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
