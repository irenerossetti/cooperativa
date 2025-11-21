from django.contrib import admin
from .models import FarmActivity, ActivityType


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']


@admin.register(FarmActivity)
class FarmActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'campaign', 'parcel', 'scheduled_date', 'status']
    list_filter = ['activity_type', 'status', 'scheduled_date']
    search_fields = ['description', 'parcel__code', 'campaign__name']
    readonly_fields = ['created_at', 'updated_at']
