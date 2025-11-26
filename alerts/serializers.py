from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = Alert
        fields = ['id', 'alert_type', 'alert_type_display', 'severity', 'severity_display',
                  'title', 'message', 'data', 'is_read', 'is_active', 'created_at', 'expires_at']
        read_only_fields = ['created_at']
