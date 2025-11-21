from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Sum
from .models import FarmActivity, ActivityType
from .serializers import (FarmActivitySerializer, FarmActivityListSerializer, 
                          ActivityTypeSerializer)
from users.permissions import IsAdminOrReadOnly


class ActivityTypeViewSet(viewsets.ModelViewSet):
    """ViewSet para tipos de labor"""
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class FarmActivityViewSet(viewsets.ModelViewSet):
    """ViewSet para labores agrícolas"""
    queryset = FarmActivity.objects.select_related('activity_type', 'campaign', 'parcel', 'created_by')
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FarmActivityListSerializer
        return FarmActivitySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        campaign = self.request.query_params.get('campaign', None)
        parcel = self.request.query_params.get('parcel', None)
        activity_type = self.request.query_params.get('activity_type', None)
        status_filter = self.request.query_params.get('status', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if campaign:
            queryset = queryset.filter(campaign_id=campaign)
        
        if parcel:
            queryset = queryset.filter(parcel_id=parcel)
        
        if activity_type:
            queryset = queryset.filter(activity_type_id=activity_type)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if date_from:
            queryset = queryset.filter(scheduled_date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(scheduled_date__lte=date_to)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Completar labor"""
        activity = self.get_object()
        activity.status = FarmActivity.COMPLETED
        activity.actual_date = request.data.get('actual_date')
        activity.completed_by = request.user
        activity.save()
        return Response({'message': 'Labor completada exitosamente'})
    
    @action(detail=False, methods=['get'])
    def report_by_campaign(self, request):
        """Reporte de labores por campaña"""
        campaign_id = request.query_params.get('campaign_id')
        if not campaign_id:
            return Response({'error': 'campaign_id es requerido'}, status=400)
        
        activities = self.queryset.filter(campaign_id=campaign_id)
        
        report = {
            'total_activities': activities.count(),
            'by_type': activities.values('activity_type__name').annotate(count=Count('id')),
            'by_status': activities.values('status').annotate(count=Count('id')),
            'total_hours': activities.aggregate(Sum('hours_worked'))['hours_worked__sum'] or 0,
        }
        
        return Response(report)
