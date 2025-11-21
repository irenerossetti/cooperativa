from django.contrib import admin
from .models import HarvestedProduct


@admin.register(HarvestedProduct)
class HarvestedProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'campaign', 'parcel', 'partner', 'quantity', 'harvest_date']
    list_filter = ['harvest_date', 'campaign', 'quality_grade']
    search_fields = ['product_name', 'parcel__code', 'partner__first_name', 'partner__last_name']
    readonly_fields = ['created_at', 'updated_at']
