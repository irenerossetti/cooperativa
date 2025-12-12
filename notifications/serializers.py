from rest_framework import serializers
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones"""
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_name', 'title', 'message', 'type', 
            'type_display', 'read', 'extra_data', 'action_url',
            'created_at', 'read_at', 'time_ago'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']

    def get_time_ago(self, obj):
        """Calcula tiempo transcurrido desde la creación"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff < timedelta(minutes=1):
            return "Ahora"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"Hace {minutes} min"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"Hace {hours}h"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"Hace {days}d"
        else:
            return obj.created_at.strftime("%d/%m/%Y")


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer para preferencias de notificación"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'email_enabled', 'push_enabled',
            'notify_sales', 'notify_payments', 'notify_stock',
            'notify_requests', 'notify_alerts', 'notify_tasks',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear notificaciones"""
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['user', 'title', 'message', 'type', 'extra_data', 'action_url']
        read_only_fields = ['user']

    def create(self, validated_data):
        notification = Notification.objects.create(**validated_data)
        
        # Aquí se puede agregar lógica para enviar push/email
        # send_push_notification(notification)
        # send_email_notification(notification)
        
        return notification
