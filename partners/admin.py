from django.contrib import admin
from .models import Partner, Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['ci', 'full_name', 'community', 'phone', 'status', 'created_at']
    list_filter = ['status', 'community', 'created_at']
    search_fields = ['ci', 'nit', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'registration_date']
