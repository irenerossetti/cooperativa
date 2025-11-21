from rest_framework import serializers
from .models import ReportType, GeneratedReport


class ReportTypeSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    
    class Meta:
        model = ReportType
        fields = ['id', 'name', 'name_display', 'description', 'is_active']


class GeneratedReportSerializer(serializers.ModelSerializer):
    report_type_name = serializers.CharField(source='report_type.get_name_display', read_only=True)
    
    class Meta:
        model = GeneratedReport
        fields = ['id', 'report_type', 'report_type_name', 'title', 'description',
                  'filters', 'file_format', 'file_path', 'file_size', 'data',
                  'generated_at', 'is_public', 'download_count']
        read_only_fields = ['generated_at', 'download_count']
