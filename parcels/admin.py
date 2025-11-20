from django.contrib import admin
from .models import Parcel, SoilType, Crop


@admin.register(SoilType)
class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'scientific_name', 'description']


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'partner', 'surface', 'soil_type', 'status', 'created_at']
    list_filter = ['status', 'soil_type', 'current_crop', 'created_at']
    search_fields = ['code', 'name', 'location', 'partner__first_name', 'partner__last_name']
    readonly_fields = ['created_at', 'updated_at']
