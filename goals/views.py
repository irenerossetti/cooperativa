from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg
from .models import Goal, GoalMilestone
from .serializers import (
    GoalSerializer,
    GoalMilestoneSerializer,
    GoalUpdateProgressSerializer
)


class GoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar metas y objetivos
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por tipo
        goal_type = self.request.query_params.get('type', None)
        if goal_type:
            queryset = queryset.filter(type=goal_type)
        
        # Filtro por estado
        goal_status = self.request.query_params.get('status', None)
        if goal_status:
            queryset = queryset.filter(status=goal_status)
        
        # Filtro por responsable
        responsible_id = self.request.query_params.get('responsible', None)
        if responsible_id:
            queryset = queryset.filter(responsible_id=responsible_id)
        
        # Solo activas (no completadas ni canceladas)
        active_only = self.request.query_params.get('active_only', None)
        if active_only and active_only.lower() == 'true':
            queryset = queryset.exclude(status__in=['COMPLETED', 'CANCELLED'])
        
        return queryset

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Actualiza el progreso de una meta"""
        goal = self.get_object()
        
        serializer = GoalUpdateProgressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_value = serializer.validated_data['current_value']
        notes = serializer.validated_data.get('notes', '')
        
        # Actualizar progreso
        goal.update_progress(new_value)
        
        if notes:
            goal.notes = notes
            goal.save()
        
        # Crear notificación si se completó
        if goal.is_completed and goal.responsible:
            from notifications.utils import create_notification
            create_notification(
                user=goal.responsible,
                title='¡Meta completada!',
                message=f'Has completado la meta: {goal.name}',
                notification_type='SUCCESS',
                extra_data={'goal_id': goal.id}
            )
        
        return Response({
            'message': 'Progreso actualizado',
            'goal': GoalSerializer(goal).data
        })

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Marca una meta como completada"""
        goal = self.get_object()
        goal.status = 'COMPLETED'
        goal.current_value = goal.target_value
        goal.save()
        
        # Notificar al responsable
        if goal.responsible:
            from notifications.utils import create_notification
            create_notification(
                user=goal.responsible,
                title='Meta completada',
                message=f'La meta "{goal.name}" ha sido marcada como completada',
                notification_type='SUCCESS',
                extra_data={'goal_id': goal.id}
            )
        
        return Response({
            'message': 'Meta marcada como completada',
            'goal': GoalSerializer(goal).data
        })

    @action(detail=False, methods=['get'])
    def at_risk(self, request):
        """Obtiene metas en riesgo"""
        goals = [goal for goal in self.get_queryset() if goal.is_at_risk]
        serializer = self.get_serializer(goals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtiene estadísticas de metas"""
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'completed': queryset.filter(status='COMPLETED').count(),
            'in_progress': queryset.filter(status='IN_PROGRESS').count(),
            'at_risk': queryset.filter(status='AT_RISK').count(),
            'not_started': queryset.filter(status='NOT_STARTED').count(),
            'cancelled': queryset.filter(status='CANCELLED').count(),
            'average_progress': 0,
            'by_type': {}
        }
        
        # Calcular progreso promedio
        goals_with_progress = [goal for goal in queryset if goal.progress_percentage > 0]
        if goals_with_progress:
            total_progress = sum(goal.progress_percentage for goal in goals_with_progress)
            stats['average_progress'] = round(total_progress / len(goals_with_progress), 2)
        
        # Por tipo
        for choice in Goal.TYPE_CHOICES:
            count = queryset.filter(type=choice[0]).count()
            if count > 0:
                stats['by_type'][choice[0]] = {
                    'label': choice[1],
                    'count': count
                }
        
        return Response(stats)


class GoalMilestoneViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar hitos de metas
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GoalMilestoneSerializer
    queryset = GoalMilestone.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrar por meta
        goal_id = self.request.query_params.get('goal', None)
        if goal_id:
            queryset = queryset.filter(goal_id=goal_id)
        
        # Solo pendientes
        pending_only = self.request.query_params.get('pending_only', None)
        if pending_only and pending_only.lower() == 'true':
            queryset = queryset.filter(completed=False)
        
        return queryset

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Marca un hito como completado"""
        milestone = self.get_object()
        milestone.mark_completed()
        
        return Response({
            'message': 'Hito marcado como completado',
            'milestone': self.get_serializer(milestone).data
        })
