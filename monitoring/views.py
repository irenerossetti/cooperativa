from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import CropMonitoring, CropAlert
from .serializers import CropMonitoringSerializer, CropAlertSerializer


class CropMonitoringViewSet(viewsets.ModelViewSet):
    """ViewSet para monitoreo de cultivos"""
    queryset = CropMonitoring.objects.all()
    serializer_class = CropMonitoringSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['parcel', 'campaign', 'phenological_stage', 'health_status', 'monitoring_date']
    search_fields = ['observations', 'recommendations']
    ordering_fields = ['monitoring_date', 'health_status']
    ordering = ['-monitoring_date']

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

    @action(detail=False, methods=['get'])
    def by_parcel(self, request):
        """Obtener monitoreos por parcela"""
        parcel_id = request.query_params.get('parcel_id')
        if not parcel_id:
            return Response({'error': 'parcel_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        monitorings = self.queryset.filter(parcel_id=parcel_id)
        serializer = self.get_serializer(monitorings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def health_summary(self, request):
        """Resumen de salud de cultivos"""
        from django.db.models import Count
        
        summary = self.queryset.values('health_status').annotate(
            count=Count('id')
        ).order_by('health_status')
        
        return Response(summary)

    @action(detail=False, methods=['get'])
    def critical_parcels(self, request):
        """Parcelas con estado crítico o malo"""
        critical = self.queryset.filter(
            health_status__in=['POOR', 'CRITICAL']
        ).order_by('-monitoring_date')
        
        serializer = self.get_serializer(critical, many=True)
        return Response(serializer.data)


class CropAlertViewSet(viewsets.ModelViewSet):
    """ViewSet para alertas de cultivos"""
    queryset = CropAlert.objects.all()
    serializer_class = CropAlertSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['monitoring', 'alert_type', 'severity', 'is_active']
    ordering_fields = ['created_at', 'severity']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolver una alerta"""
        alert = self.get_object()
        resolution_notes = request.data.get('resolution_notes', '')
        
        from django.utils import timezone
        alert.is_active = False
        alert.resolved_at = timezone.now()
        alert.resolution_notes = resolution_notes
        alert.save()
        
        serializer = self.get_serializer(alert)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active_alerts(self, request):
        """Obtener alertas activas"""
        active = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_severity(self, request):
        """Alertas agrupadas por severidad"""
        from django.db.models import Count
        
        summary = self.queryset.filter(is_active=True).values('severity').annotate(
            count=Count('id')
        ).order_by('severity')
        
        return Response(summary)
