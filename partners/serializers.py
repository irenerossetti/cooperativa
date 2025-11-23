from rest_framework import serializers
from .models import Partner, Community


class CommunitySerializer(serializers.ModelSerializer):
    """Serializer para comunidades"""
    partners_count = serializers.IntegerField(source='partners.count', read_only=True)
    
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'is_active', 'partners_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PartnerSerializer(serializers.ModelSerializer):
    """Serializer para socios"""
    community_name = serializers.CharField(source='community.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    total_parcels = serializers.IntegerField(read_only=True)
    total_surface = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Partner
        fields = ['id', 'ci', 'nit', 'first_name', 'last_name', 'full_name', 'email', 'phone', 
                  'address', 'community', 'community_name', 'user', 'status', 'status_display',
                  'registration_date', 'notes', 'total_parcels', 'total_surface', 
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'registration_date']

    def validate_ci(self, value):
        """Validar que el CI no esté duplicado"""
        partner_id = self.instance.id if self.instance else None
        if Partner.objects.filter(ci=value).exclude(id=partner_id).exists():
            raise serializers.ValidationError("Este CI ya está registrado.")
        return value

    def validate_nit(self, value):
        """Validar que el NIT no esté duplicado"""
        if not value:
            return value
        partner_id = self.instance.id if self.instance else None
        if Partner.objects.filter(nit=value).exclude(id=partner_id).exists():
            raise serializers.ValidationError("Este NIT ya está registrado.")
        return value

    def validate_email(self, value):
        """Validar formato de email"""
        if value and '@' not in value:
            raise serializers.ValidationError("Formato de email inválido.")
        return value


class PartnerListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de socios"""
    community_name = serializers.CharField(source='community.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Partner
        fields = ['id', 'ci', 'first_name', 'last_name', 'full_name', 'phone', 'email', 'community', 'community_name', 'status', 'status_display']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
