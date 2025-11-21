from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Shipment
from .serializers import ShipmentSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.select_related('order', 'destination_community')
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        order = self.request.query_params.get('order', None)
        status_filter = self.request.query_params.get('status', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if order:
            queryset = queryset.filter(order_id=order)
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
    def schedule(self, request, pk=None):
        shipment = self.get_object()
        scheduled_date = request.data.get('scheduled_date')
        
        if not scheduled_date:
            return Response({'error': 'scheduled_date es requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        shipment.scheduled_date = scheduled_date
        shipment.status = Shipment.SCHEDULED
        shipment.save()
        
        return Response({'message': 'Envío programado exitosamente'})
    
    @action(detail=True, methods=['post'])
    def mark_in_transit(self, request, pk=None):
        shipment = self.get_object()
        shipment.status = Shipment.IN_TRANSIT
        shipment.save()
        return Response({'message': 'Envío marcado como en tránsito'})
    
    @action(detail=True, methods=['post'])
    def mark_delivered(self, request, pk=None):
        shipment = self.get_object()
        actual_delivery_date = request.data.get('actual_delivery_date')
        received_by = request.data.get('received_by')
        signature = request.data.get('signature')
        
        shipment.status = Shipment.DELIVERED
        if actual_delivery_date:
            shipment.actual_delivery_date = actual_delivery_date
        if received_by:
            shipment.received_by = received_by
        if signature:
            shipment.signature = signature
        
        shipment.save()
        return Response({'message': 'Envío marcado como entregado'})
    
    @action(detail=False, methods=['get'])
    def pending_shipments(self, request):
        shipments = self.queryset.filter(status__in=[Shipment.PENDING, Shipment.SCHEDULED])
        serializer = self.get_serializer(shipments, many=True)
        return Response(serializer.data)
