from django.contrib import admin
from .models import Organization, OrganizationMember


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'subdomain', 'plan', 'status', 'is_active', 'created_at']
    list_filter = ['plan', 'status', 'is_active', 'created_at']
    search_fields = ['name', 'subdomain', 'email']
    readonly_fields = ['created_at', 'updated_at', 'slug']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'subdomain', 'email', 'phone', 'address')
        }),
        ('Plan y Estado', {
            'fields': ('plan', 'status', 'is_active')
        }),
        ('Límites', {
            'fields': ('max_users', 'max_products', 'max_storage_mb')
        }),
        ('Fechas', {
            'fields': ('trial_ends_at', 'subscription_ends_at', 'created_at', 'updated_at')
        }),
        ('Configuración', {
            'fields': ('settings',),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'is_active', 'joined_at']
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['user__username', 'user__email', 'organization__name']
    raw_id_fields = ['user', 'organization']
