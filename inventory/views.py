from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum
from .models import InventoryItem, InventoryMovement, InventoryCategory, StockAlert
from .serializers import (InventoryItemSerializer, InventoryMovementSerializer,
                          InventoryCategorySerializer, StockAlertSerializer)
from users.permissions import IsAdminOrReadOnly


class InventoryCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para categorías de inventario"""
    queryset = InventoryCategory.objects.all()
    serializer_class = InventoryCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class InventoryItemViewSet(viewsets.ModelViewSet):
    """ViewSet para items de inventario"""
    queryset = InventoryItem.objects.select_related('category')
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        low_stock = self.request.query_params.get('low_stock', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(name__icontains=search) |
                Q(species__icontains=search)
            )
        
        if low_stock == 'true':
            queryset = [item for item in queryset if item.is_low_stock]
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def low_stock_items(self, request):
        """Items con stock bajo"""
        items = [item for item in self.queryset if item.is_low_stock]
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def availability(self, request):
        """Consultar disponibilidad de insumos"""
        category = request.query_params.get('category')
        queryset = self.queryset.filter(is_active=True)
        
        if category:
            queryset = queryset.filter(category__name=category)
        
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'code': item.code,
                'name': item.name,
                'current_stock': item.current_stock,
                'unit_of_measure': item.unit_of_measure,
                'status': item.stock_status
            })
        
        return Response(data)


class InventoryMovementViewSet(viewsets.ModelViewSet):
    """ViewSet para movimientos de inventario"""
    queryset = InventoryMovement.objects.select_related('item', 'created_by')
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        item = self.request.query_params.get('item', None)
        movement_type = self.request.query_params.get('movement_type', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if item:
            queryset = queryset.filter(item_id=item)
        
        if movement_type:
            queryset = queryset.filter(movement_type=movement_type)
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def report(self, request):
        """Reporte de movimientos de inventario"""
        item_id = request.query_params.get('item_id')
        
        if item_id:
            movements = self.queryset.filter(item_id=item_id)
        else:
            movements = self.queryset
        
        report = {
            'total_entries': movements.filter(movement_type='ENTRY').aggregate(Sum('quantity'))['quantity__sum'] or 0,
            'total_exits': movements.filter(movement_type='EXIT').aggregate(Sum('quantity'))['quantity__sum'] or 0,
            'total_movements': movements.count(),
        }
        
        return Response(report)


class StockAlertViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para alertas de stock (solo lectura)"""
    queryset = StockAlert.objects.select_related('item')
    serializer_class = StockAlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        is_resolved = self.request.query_params.get('is_resolved', None)
        
        if is_resolved is not None:
            queryset = queryset.filter(is_resolved=is_resolved.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Marcar alerta como resuelta"""
        alert = self.get_object()
        alert.is_resolved = True
        from django.utils import timezone
        alert.resolved_date = timezone.now()
        alert.save()
        return Response({'message': 'Alerta resuelta'})
