from django.contrib import admin
from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'alert_type', 'severity', 'is_read', 'is_active', 'created_at', 'organization']
    list_filter = ['alert_type', 'severity', 'is_read', 'is_active', 'created_at']
    search_fields = ['title', 'message']
    date_hierarchy = 'created_at'
