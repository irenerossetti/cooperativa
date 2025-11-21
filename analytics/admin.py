from django.contrib import admin
from .models import PriceTrend, DemandTrend


@admin.register(PriceTrend)
class PriceTrendAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'date', 'average_price', 'trend_direction']
    list_filter = ['trend_direction', 'date']


@admin.register(DemandTrend)
class DemandTrendAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'date', 'demand_level', 'trend_direction']
    list_filter = ['demand_level', 'trend_direction', 'date']
