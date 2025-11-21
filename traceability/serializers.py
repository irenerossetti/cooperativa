from rest_framework import serializers
from .models import ParcelTraceability, InputUsageRecord


class ParcelTraceabilitySerializer(serializers.ModelSerializer):
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    
    class Meta:
        model = ParcelTraceability
        fields = ['id', 'parcel', 'parcel_code', 'campaign', 'campaign_name',
                  'traceability_code', 'start_date', 'end_date', 'total_activities',
                  'total_inputs_used', 'total_production', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class InputUsageRecordSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='inventory_item.name', read_only=True)
    
    class Meta:
        model = InputUsageRecord
        fields = ['id', 'traceability', 'inventory_item', 'item_name', 'farm_activity',
                  'application_date', 'quantity_used', 'application_method', 'purpose',
                  'weather_conditions', 'notes', 'recorded_at']
        read_only_fields = ['recorded_at']
