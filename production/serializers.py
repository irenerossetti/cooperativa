from rest_framework import serializers
from .models import HarvestedProduct


class HarvestedProductSerializer(serializers.ModelSerializer):
    """Serializer para productos cosechados"""
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)
    yield_per_hectare = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = HarvestedProduct
        fields = ['id', 'campaign', 'campaign_name', 'parcel', 'parcel_code', 'partner',
                  'partner_name', 'product_name', 'harvest_date', 'quantity', 'quality_grade',
                  'moisture_percentage', 'temperature', 'storage_location', 'observations',
                  'yield_per_hectare', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """Validar que la parcela pertenezca a la campaña"""
        campaign = data.get('campaign')
        parcel = data.get('parcel')
        
        if campaign and parcel and parcel not in campaign.parcels.all():
            raise serializers.ValidationError({
                "parcel": "La parcela no pertenece a esta campaña."
            })
        
        return data


class HarvestedProductListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado"""
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)
    
    class Meta:
        model = HarvestedProduct
        fields = ['id', 'product_name', 'parcel_code', 'partner_name', 'harvest_date', 'quantity']
