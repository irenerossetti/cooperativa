from django.contrib import admin
from .models import ParcelTraceability, InputUsageRecord


@admin.register(ParcelTraceability)
class ParcelTraceabilityAdmin(admin.ModelAdmin):
    list_display = ['traceability_code', 'parcel', 'campaign', 'start_date', 'is_active']
    list_filter = ['is_active', 'start_date']


@admin.register(InputUsageRecord)
class InputUsageRecordAdmin(admin.ModelAdmin):
    list_display = ['traceability', 'inventory_item', 'application_date', 'quantity_used']
    list_filter = ['application_date']
