from django.contrib import admin
from .models import InventoryItem, InventoryMovement, InventoryCategory, StockAlert


@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'current_stock', 'minimum_stock', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['code', 'name', 'species', 'variety']


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ['item', 'movement_type', 'quantity', 'date', 'created_by']
    list_filter = ['movement_type', 'date']
    search_fields = ['item__name', 'reference']


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ['item', 'current_stock', 'minimum_stock', 'is_resolved', 'alert_date']
    list_filter = ['is_resolved', 'alert_date']
