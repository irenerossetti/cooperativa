from django.contrib import admin
from .models import ReportType, GeneratedReport


@admin.register(ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'file_format', 'generated_at', 'download_count']
    list_filter = ['report_type', 'file_format', 'generated_at']
