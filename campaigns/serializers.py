from rest_framework import serializers
from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    """Serializer para campañas"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_area = serializers.ReadOnlyField()
    total_partners = serializers.ReadOnlyField()
    partners_count = serializers.SerializerMethodField()
    parcels_count = serializers.SerializerMethodField()
    
    def get_partners_count(self, obj):
        return obj.partners.count()
    
    def get_parcels_count(self, obj):
        return obj.parcels.count()
    
    class Meta:
        model = Campaign
        fields = ['id', 'code', 'name', 'description', 'start_date', 'end_date', 
                  'actual_end_date', 'target_area', 'target_production', 'status', 
                  'status_display', 'partners', 'parcels', 'partners_count', 'parcels_count',
                  'total_area', 'total_partners', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_code(self, value):
        """Validar que el código no esté duplicado"""
        campaign_id = self.instance.id if self.instance else None
        if Campaign.objects.filter(code=value).exclude(id=campaign_id).exists():
            raise serializers.ValidationError("Este código de campaña ya está registrado.")
        return value

    def validate(self, data):
        """Validar fechas"""
        if 'start_date' in data and 'end_date' in data:
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError({
                    "end_date": "La fecha de fin debe ser posterior a la fecha de inicio."
                })
        return data


class CampaignListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de campañas"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    partners_count = serializers.SerializerMethodField()
    parcels_count = serializers.SerializerMethodField()
    
    def get_partners_count(self, obj):
        return obj.partners.count()
    
    def get_parcels_count(self, obj):
        return obj.parcels.count()
    
    class Meta:
        model = Campaign
        fields = ['id', 'code', 'name', 'start_date', 'end_date', 'status', 
                  'status_display', 'partners_count', 'parcels_count']
