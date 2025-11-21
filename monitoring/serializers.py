from rest_framework import serializers
from .models import CropMonitoring, CropAlert


class CropAlertSerializer(serializers.ModelSerializer):
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = CropAlert
        fields = ['id', 'monitoring', 'alert_type', 'alert_type_display', 'severity',
                  'severity_display', 'title', 'description', 'is_active', 'resolved_at',
                  'resolution_notes', 'created_at']
        read_only_fields = ['created_at']


class CropMonitoringSerializer(serializers.ModelSerializer):
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    phenological_stage_display = serializers.CharField(source='get_phenological_stage_display', read_only=True)
    health_status_display = serializers.CharField(source='get_health_status_display', read_only=True)
    alerts = CropAlertSerializer(many=True, read_only=True)
    
    class Meta:
        model = CropMonitoring
        fields = ['id', 'parcel', 'parcel_code', 'campaign', 'campaign_name',
                  'phenological_stage', 'phenological_stage_display', 'health_status',
                  'health_status_display', 'plant_height', 'leaf_color_index', 'soil_moisture',
                  'temperature', 'pest_presence', 'disease_presence', 'pest_details',
                  'disease_details', 'observations', 'recommendations', 'images',
                  'monitoring_date', 'alerts', 'recorded_at']
        read_only_fields = ['recorded_at']
