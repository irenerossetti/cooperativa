from rest_framework import serializers
from .models import FarmActivity, ActivityType


class ActivityTypeSerializer(serializers.ModelSerializer):
    """Serializer para tipos de labor"""
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    
    class Meta:
        model = ActivityType
        fields = ['id', 'name', 'name_display', 'description', 'is_active', 
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class FarmActivitySerializer(serializers.ModelSerializer):
    """Serializer para labores agrícolas"""
    activity_type_name = serializers.CharField(source='activity_type.get_name_display', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = FarmActivity
        fields = ['id', 'activity_type', 'activity_type_name', 'campaign', 'campaign_name',
                  'parcel', 'parcel_code', 'scheduled_date', 'actual_date', 'description',
                  'quantity', 'area_covered', 'workers_count', 'hours_worked', 'status',
                  'status_display', 'observations', 'weather_conditions', 'completed_by',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """Validar fechas"""
        if 'actual_date' in data and 'scheduled_date' in data:
            if data['actual_date'] < data['scheduled_date']:
                raise serializers.ValidationError({
                    "actual_date": "La fecha real no puede ser anterior a la fecha programada."
                })
        return data


class FarmActivityListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado"""
    activity_type_name = serializers.CharField(source='activity_type.get_name_display', read_only=True)
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = FarmActivity
        fields = ['id', 'activity_type_name', 'parcel_code', 'scheduled_date', 
                  'status', 'status_display']
