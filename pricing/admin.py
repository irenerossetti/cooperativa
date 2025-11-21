from django.contrib import admin
from .models import PriceList, PriceListItem


class PriceListItemInline(admin.TabularInline):
    model = PriceListItem
    extra = 1


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'campaign', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'campaign', 'start_date']
    search_fields = ['code', 'name']
    inlines = [PriceListItemInline]


@admin.register(PriceListItem)
class PriceListItemAdmin(admin.ModelAdmin):
    list_display = ['price_list', 'product_name', 'unit_price', 'is_active']
    list_filter = ['is_active', 'price_list']
    search_fields = ['product_name']
