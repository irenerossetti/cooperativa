from rest_framework import serializers
from .models import Event, EventReminder


class EventSerializer(serializers.ModelSerializer):
    """Serializer para eventos"""
    
    # Campos para el frontend (coinciden con EventsCalendar.jsx)
    event_date = serializers.DateTimeField(source='start_datetime')
    max_participants = serializers.IntegerField(required=False, allow_null=True, default=None, read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_date', 'location',
            'max_participants', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'max_participants']
    
    def create(self, validated_data):
        # Mapear event_date a start_datetime y end_datetime
        start_datetime = validated_data.pop('start_datetime')
        from datetime import timedelta
        validated_data['start_datetime'] = start_datetime
        validated_data['end_datetime'] = start_datetime + timedelta(hours=1)  # Por defecto, 1 hora
        validated_data['type'] = 'OTRO'  # Tipo por defecto
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Mapear event_date a start_datetime
        if 'start_datetime' in validated_data:
            start_datetime = validated_data.pop('start_datetime')
            from datetime import timedelta
            validated_data['start_datetime'] = start_datetime
            validated_data['end_datetime'] = start_datetime + timedelta(hours=1)
        return super().update(instance, validated_data)


class EventReminderSerializer(serializers.ModelSerializer):
    """Serializer para recordatorios"""
    
    event_title = serializers.CharField(source='event.title', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = EventReminder
        fields = ['id', 'event', 'event_title', 'user', 'user_name', 'sent_at', 'method']
        read_only_fields = ['id', 'sent_at']


class EventCalendarSerializer(serializers.ModelSerializer):
    """Serializer simplificado para vista de calendario"""
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'type', 'start_datetime', 'end_datetime',
            'all_day', 'color', 'completed', 'priority'
        ]
