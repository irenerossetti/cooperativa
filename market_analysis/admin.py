from django.contrib import admin
from .models import MarketPrice, PriceAlert


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['product_type', 'price_per_kg', 'date', 'source', 'organization']
    list_filter = ['product_type', 'date', 'organization']
    search_fields = ['product_type', 'source']
    date_hierarchy = 'date'


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ['product_type', 'alert_type', 'percentage_change', 'is_active', 'created_at', 'organization']
    list_filter = ['alert_type', 'is_active', 'created_at', 'organization']
    search_fields = ['product_type', 'message']
    date_hierarchy = 'created_at'
