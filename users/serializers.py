from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    """Serializer para roles"""
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuarios"""
    role_name = serializers.CharField(source='role.get_name_display', read_only=True)
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    partner = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                  'role', 'role_name', 'is_active', 'is_staff', 'is_superuser', 
                  'password', 'created_at', 'updated_at', 'partner']
        read_only_fields = ['created_at', 'updated_at', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_partner(self, obj):
        """Obtener información del partner asociado con su organización"""
        try:
            if hasattr(obj, 'partner') and obj.partner:
                return {
                    'id': obj.partner.id,
                    'full_name': obj.partner.full_name,
                    'organization': {
                        'id': obj.partner.organization.id,
                        'name': obj.partner.organization.name,
                        'subdomain': obj.partner.organization.subdomain,
                    } if obj.partner.organization else None
                }
        except:
            pass
        return None

    def validate_email(self, value):
        """Validar que el email no esté duplicado"""
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value

    def validate_username(self, value):
        """Validar que el username no esté duplicado"""
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(username=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está registrado.")
        return value

    def create(self, validated_data):
        """Crear usuario con contraseña encriptada"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Actualizar usuario"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambio de contraseña"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
