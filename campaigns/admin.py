from django.contrib import admin
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'start_date', 'end_date', 'status', 'created_at']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['code', 'name', 'description']
    filter_horizontal = ['partners', 'parcels']
    readonly_fields = ['created_at', 'updated_at']
