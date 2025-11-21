from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import PaymentMethod, Customer, Order, OrderItem, Payment
from .serializers import (PaymentMethodSerializer, CustomerSerializer, 
                          OrderSerializer, OrderItemSerializer, PaymentSerializer)
from users.permissions import IsAdminOrReadOnly


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.select_related('partner')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(document_number__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer', 'campaign').prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        customer = self.request.query_params.get('customer', None)
        campaign = self.request.query_params.get('campaign', None)
        status_filter = self.request.query_params.get('status', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if customer:
            queryset = queryset.filter(customer_id=customer)
        if campaign:
            queryset = queryset.filter(campaign_id=campaign)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if date_from:
            queryset = queryset.filter(order_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(order_date__lte=date_to)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.status != Order.DRAFT:
            return Response({'error': 'Solo se pueden confirmar pedidos en borrador'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar stock y descontar
        for item in order.items.all():
            product = item.product
            if product.quantity < item.quantity:
                return Response({'error': f'Stock insuficiente para {product.product_name}'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            product.quantity -= item.quantity
            product.save()
        
        order.status = Order.CONFIRMED
        order.save()
        return Response({'message': 'Pedido confirmado exitosamente'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.status = Order.CANCELLED
        order.save()
        return Response({'message': 'Pedido cancelado'})
    
    @action(detail=False, methods=['get'])
    def sales_report(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        orders = self.queryset.filter(status__in=[Order.CONFIRMED, Order.PAID, Order.DELIVERED])
        if date_from:
            orders = orders.filter(order_date__gte=date_from)
        if date_to:
            orders = orders.filter(order_date__lte=date_to)
        
        report = {
            'total_orders': orders.count(),
            'total_sales': orders.aggregate(Sum('total'))['total__sum'] or 0,
            'by_status': orders.values('status').annotate(count=Count('id'), total=Sum('total')),
            'by_customer': orders.values('customer__name').annotate(count=Count('id'), total=Sum('total'))[:10],
        }
        return Response(report)
    
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        orders = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="ventas_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Número', 'Cliente', 'Fecha', 'Total', 'Estado'])
        
        for order in orders:
            writer.writerow([order.order_number, order.customer.name, order.order_date, 
                           order.total, order.get_status_display()])
        
        return response


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order', 'product')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('order', 'payment_method')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def payment_history(self, request):
        order_id = request.query_params.get('order_id')
        if order_id:
            payments = self.queryset.filter(order_id=order_id)
        else:
            payments = self.queryset
        
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)
