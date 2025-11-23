from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Sum
from .models import Campaign
from .serializers import CampaignSerializer, CampaignListSerializer
from users.permissions import IsAdminOrReadOnly


class CampaignViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de campañas"""
    queryset = Campaign.objects.prefetch_related('partners', 'parcels')
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CampaignListSerializer
        return CampaignSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        search = self.request.query_params.get('search', None)
        status_filter = self.request.query_params.get('status', None)
        partner = self.request.query_params.get('partner', None)
        year = self.request.query_params.get('year', None)
        
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if partner:
            queryset = queryset.filter(partners__id=partner)
        
        if year:
            queryset = queryset.filter(start_date__year=year)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activar campaña"""
        campaign = self.get_object()
        campaign.status = Campaign.ACTIVE
        campaign.save()
        return Response({'message': 'Campaña activada exitosamente'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Completar campaña"""
        campaign = self.get_object()
        campaign.status = Campaign.COMPLETED
        campaign.actual_end_date = request.data.get('actual_end_date')
        campaign.save()
        return Response({'message': 'Campaña completada exitosamente'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancelar campaña"""
        campaign = self.get_object()
        campaign.status = Campaign.CANCELLED
        campaign.save()
        return Response({'message': 'Campaña cancelada exitosamente'})
    
    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Reporte de campaña"""
        campaign = self.get_object()
        
        # Aquí puedes agregar más estadísticas
        data = {
            'campaign': CampaignSerializer(campaign).data,
            'statistics': {
                'total_partners': campaign.partners.count(),
                'total_parcels': campaign.parcels.count(),
                'total_area': campaign.total_area,
                'target_production': campaign.target_production,
            }
        }
        return Response(data)
