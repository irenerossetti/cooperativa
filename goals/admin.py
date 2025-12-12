from django.contrib import admin
from .models import Goal, GoalMilestone


class GoalMilestoneInline(admin.TabularInline):
    model = GoalMilestone
    extra = 1
    fields = ['title', 'target_date', 'completed']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'progress_display', 'status', 'responsible', 'end_date']
    list_filter = ['type', 'status', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage']
    inlines = [GoalMilestoneInline]
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description', 'type')
        }),
        ('Valores', {
            'fields': ('target_value', 'current_value', 'unit', 'progress_percentage')
        }),
        ('Fechas', {
            'fields': ('start_date', 'end_date')
        }),
        ('Responsable y estado', {
            'fields': ('responsible', 'status')
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
    
    def progress_display(self, obj):
        return f"{obj.progress_percentage}%"
    progress_display.short_description = 'Progreso'


@admin.register(GoalMilestone)
class GoalMilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal', 'target_date', 'completed']
    list_filter = ['completed', 'target_date']
    search_fields = ['title', 'goal__name']
    readonly_fields = ['completed_at', 'created_at', 'updated_at']
