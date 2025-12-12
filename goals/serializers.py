from rest_framework import serializers
from .models import Goal, GoalMilestone


class GoalMilestoneSerializer(serializers.ModelSerializer):
    """Serializer para hitos"""
    
    class Meta:
        model = GoalMilestone
        fields = [
            'id', 'goal', 'title', 'description', 'target_date',
            'completed', 'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'completed_at', 'created_at', 'updated_at']


class GoalSerializer(serializers.ModelSerializer):
    """Serializer para metas"""
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    responsible_name = serializers.CharField(source='responsible.get_full_name', read_only=True)
    
    # Propiedades calculadas
    progress_percentage = serializers.FloatField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    is_at_risk = serializers.BooleanField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    
    # Hitos
    milestones = GoalMilestoneSerializer(many=True, read_only=True)
    milestones_count = serializers.SerializerMethodField()
    completed_milestones = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = [
            'id', 'name', 'description', 'type', 'type_display',
            'target_value', 'current_value', 'unit',
            'start_date', 'end_date', 'responsible', 'responsible_name',
            'status', 'status_display', 'notes',
            'progress_percentage', 'is_completed', 'is_at_risk', 'days_remaining',
            'milestones', 'milestones_count', 'completed_milestones',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_milestones_count(self, obj):
        return obj.milestones.count()
    
    def get_completed_milestones(self, obj):
        return obj.milestones.filter(completed=True).count()


class GoalUpdateProgressSerializer(serializers.Serializer):
    """Serializer para actualizar progreso"""
    
    current_value = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
