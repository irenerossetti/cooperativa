from rest_framework import serializers
from .models import Organization, OrganizationMember
from django.contrib.auth import get_user_model

User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    plan_display = serializers.CharField(source='get_plan_display_name', read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'slug', 'subdomain', 'email', 'phone', 'address',
            'plan', 'plan_display', 'status', 'max_users', 'max_products',
            'max_storage_mb', 'is_active', 'created_at', 'trial_ends_at',
            'subscription_ends_at', 'member_count'
        ]
        read_only_fields = ['slug', 'created_at']
    
    def get_member_count(self, obj):
        return obj.members.filter(is_active=True).count()


class OrganizationRegistrationSerializer(serializers.Serializer):
    """Serializer para registro de nueva organización con usuario propietario"""
    
    # Datos de la organización
    organization_name = serializers.CharField(max_length=200)
    subdomain = serializers.SlugField(max_length=63)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Datos del usuario propietario
    username = serializers.CharField(max_length=150)
    user_email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    
    def validate_subdomain(self, value):
        if Organization.objects.filter(subdomain=value).exists():
            raise serializers.ValidationError('Este subdominio ya está en uso.')
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Este nombre de usuario ya está en uso.')
        return value
    
    def validate_user_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este email ya está registrado.')
        return value
    
    def create(self, validated_data):
        from datetime import timedelta
        from django.utils import timezone
        
        # Crear la organización
        organization = Organization.objects.create(
            name=validated_data['organization_name'],
            subdomain=validated_data['subdomain'],
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
            plan='FREE',
            status='TRIAL',
            trial_ends_at=timezone.now() + timedelta(days=30),
            max_users=5,
            max_products=100,
            max_storage_mb=100
        )
        
        # Crear el usuario propietario
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['user_email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        # Crear la membresía como propietario
        OrganizationMember.objects.create(
            organization=organization,
            user=user,
            role='OWNER',
            is_active=True
        )
        
        return {
            'organization': organization,
            'user': user
        }


class OrganizationMemberSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    
    class Meta:
        model = OrganizationMember
        fields = [
            'id', 'organization', 'organization_name', 'user', 'user_username',
            'user_email', 'user_full_name', 'role', 'is_active', 'joined_at'
        ]
        read_only_fields = ['joined_at']
    
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
