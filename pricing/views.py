from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date
from .models import PriceList, PriceListItem
from .serializers import PriceListSerializer, PriceListItemSerializer
from users.permissions import IsAdminOrReadOnly


class PriceListViewSet(viewsets.ModelViewSet):
    queryset = PriceList.objects.select_related('campaign').prefetch_related('items')
    serializer_class = PriceListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        campaign = self.request.query_params.get('campaign', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if campaign:
            queryset = queryset.filter(campaign_id=campaign)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active_for_campaign(self, request):
        campaign_id = request.query_params.get('campaign_id')
        today = date.today()
        
        if not campaign_id:
            return Response({'error': 'campaign_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        price_list = self.queryset.filter(
            campaign_id=campaign_id,
            is_active=True,
            start_date__lte=today,
            end_date__gte=today
        ).first()
        
        if price_list:
            serializer = self.get_serializer(price_list)
            return Response(serializer.data)
        
        return Response({'error': 'No hay lista de precios vigente para esta campaña'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def get_price(self, request, pk=None):
        price_list = self.get_object()
        product_name = request.query_params.get('product_name')
        quantity = float(request.query_params.get('quantity', 1))
        
        if not product_name:
            return Response({'error': 'product_name es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        item = price_list.items.filter(product_name=product_name, is_active=True).first()
        
        if item:
            price = item.get_price_for_quantity(quantity)
            return Response({
                'product_name': product_name,
                'unit_price': item.unit_price,
                'final_price': price,
                'discount_applied': item.discount_percentage if quantity >= (item.min_quantity or 0) else 0
            })
        
        return Response({'error': 'Producto no encontrado en la lista de precios'}, 
                       status=status.HTTP_404_NOT_FOUND)


class PriceListItemViewSet(viewsets.ModelViewSet):
    queryset = PriceListItem.objects.select_related('price_list')
    serializer_class = PriceListItemSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        price_list = self.request.query_params.get('price_list', None)
        
        if price_list:
            queryset = queryset.filter(price_list_id=price_list)
        
        return queryset
