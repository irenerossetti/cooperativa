from django.contrib import admin
from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['shipment_number', 'order', 'scheduled_date', 'status', 'carrier']
    list_filter = ['status', 'scheduled_date']
    search_fields = ['shipment_number', 'order__order_number', 'tracking_number']
    readonly_fields = ['created_at', 'updated_at']
