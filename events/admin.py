from django.contrib import admin
from .models import Event, EventReminder


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'start_datetime', 'priority', 'completed', 'created_by']
    list_filter = ['type', 'priority', 'completed', 'start_datetime']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['parcels', 'participants']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'type', 'description', 'priority')
        }),
        ('Fechas y horarios', {
            'fields': ('start_datetime', 'end_datetime', 'all_day')
        }),
        ('Ubicación', {
            'fields': ('location',)
        }),
        ('Relaciones', {
            'fields': ('parcels', 'participants', 'created_by')
        }),
        ('Estado', {
            'fields': ('completed', 'color')
        }),
        ('Recordatorios', {
            'fields': ('reminder_sent', 'reminder_minutes')
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Fechas del sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EventReminder)
class EventReminderAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'method', 'sent_at']
    list_filter = ['method', 'sent_at']
    search_fields = ['event__title', 'user__username']
    readonly_fields = ['sent_at']
