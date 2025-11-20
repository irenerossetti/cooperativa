from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer para registros de auditoría"""
    username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'username', 'action', 'action_display', 'model_name', 
                  'object_id', 'description', 'ip_address', 'timestamp']
        read_only_fields = ['id', 'timestamp']
