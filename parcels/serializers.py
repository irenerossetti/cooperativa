from rest_framework import serializers
from .models import Parcel, SoilType, Crop


class SoilTypeSerializer(serializers.ModelSerializer):
    """Serializer para tipos de suelo"""
    
    class Meta:
        model = SoilType
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CropSerializer(serializers.ModelSerializer):
    """Serializer para cultivos"""
    
    class Meta:
        model = Crop
        fields = ['id', 'name', 'scientific_name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ParcelSerializer(serializers.ModelSerializer):
    """Serializer para parcelas"""
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)
    soil_type_name = serializers.CharField(source='soil_type.name', read_only=True)
    crop_name = serializers.CharField(source='current_crop.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Parcel
        fields = ['id', 'code', 'name', 'surface', 'location', 'latitude', 'longitude',
                  'partner', 'partner_name', 'soil_type', 'soil_type_name', 
                  'current_crop', 'crop_name', 'status', 'status_display', 'notes',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_code(self, value):
        """Validar que el código no esté duplicado"""
        parcel_id = self.instance.id if self.instance else None
        if Parcel.objects.filter(code=value).exclude(id=parcel_id).exists():
            raise serializers.ValidationError("Este código de parcela ya está registrado.")
        return value

    def validate_surface(self, value):
        """Validar que la superficie sea positiva"""
        if value <= 0:
            raise serializers.ValidationError("La superficie debe ser mayor a 0.")
        return value


class ParcelListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de parcelas"""
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)
    soil_type_name = serializers.CharField(source='soil_type.name', read_only=True)
    
    class Meta:
        model = Parcel
        fields = ['id', 'code', 'name', 'surface', 'partner_name', 'soil_type_name', 'status']
