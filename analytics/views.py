from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from .models import PriceTrend, DemandTrend
from .serializers import PriceTrendSerializer, DemandTrendSerializer


class PriceTrendViewSet(viewsets.ModelViewSet):
    queryset = PriceTrend.objects.all()
    serializer_class = PriceTrendSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_product(self, request):
        """Tendencias de precio por producto"""
        product_name = request.query_params.get('product_name')
        if not product_name:
            return Response({'error': 'product_name es requerido'}, status=400)
        
        trends = self.queryset.filter(product_name=product_name).order_by('-date')[:30]
        serializer = self.get_serializer(trends, many=True)
        return Response(serializer.data)


class DemandTrendViewSet(viewsets.ModelViewSet):
    queryset = DemandTrend.objects.all()
    serializer_class = DemandTrendSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def market_analysis(self, request):
        """Análisis de mercado"""
        product_name = request.query_params.get('product_name')
        
        if product_name:
            trends = self.queryset.filter(product_name=product_name)
        else:
            trends = self.queryset
        
        analysis = {
            'avg_demand_index': trends.aggregate(Avg('demand_index'))['demand_index__avg'] or 0,
            'high_demand_count': trends.filter(demand_level='HIGH').count(),
            'trends': self.get_serializer(trends[:10], many=True).data
        }
        return Response(analysis)
