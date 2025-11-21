from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Avg, Count
from .models import HarvestedProduct
from .serializers import HarvestedProductSerializer, HarvestedProductListSerializer


class HarvestedProductViewSet(viewsets.ModelViewSet):
    """ViewSet para productos cosechados"""
    queryset = HarvestedProduct.objects.select_related('campaign', 'parcel', 'partner')
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return HarvestedProductListSerializer
        return HarvestedProductSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        campaign = self.request.query_params.get('campaign', None)
        parcel = self.request.query_params.get('parcel', None)
        partner = self.request.query_params.get('partner', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if campaign:
            queryset = queryset.filter(campaign_id=campaign)
        
        if parcel:
            queryset = queryset.filter(parcel_id=parcel)
        
        if partner:
            queryset = queryset.filter(partner_id=partner)
        
        if date_from:
            queryset = queryset.filter(harvest_date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(harvest_date__lte=date_to)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def report_by_campaign(self, request):
        """Reporte de producción por campaña"""
        campaign_id = request.query_params.get('campaign_id')
        if not campaign_id:
            return Response({'error': 'campaign_id es requerido'}, status=400)
        
        products = self.queryset.filter(campaign_id=campaign_id)
        
        report = {
            'total_quantity': products.aggregate(Sum('quantity'))['quantity__sum'] or 0,
            'total_products': products.count(),
            'by_parcel': products.values('parcel__code').annotate(
                total=Sum('quantity'),
                count=Count('id')
            ),
            'by_partner': products.values('partner__first_name', 'partner__last_name').annotate(
                total=Sum('quantity'),
                count=Count('id')
            ),
            'average_yield': products.aggregate(Avg('quantity'))['quantity__avg'] or 0,
        }
        
        return Response(report)
    
    @action(detail=False, methods=['get'])
    def report_by_parcel(self, request):
        """Reporte de producción por parcela"""
        parcel_id = request.query_params.get('parcel_id')
        if not parcel_id:
            return Response({'error': 'parcel_id es requerido'}, status=400)
        
        products = self.queryset.filter(parcel_id=parcel_id)
        
        report = {
            'total_quantity': products.aggregate(Sum('quantity'))['quantity__sum'] or 0,
            'total_harvests': products.count(),
            'by_campaign': products.values('campaign__name').annotate(
                total=Sum('quantity'),
                count=Count('id')
            ),
            'by_product': products.values('product_name').annotate(
                total=Sum('quantity'),
                count=Count('id')
            ),
        }
        
        return Response(report)
