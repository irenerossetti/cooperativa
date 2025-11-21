from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg
from .models import ExpenseCategory, FieldExpense, ParcelProfitability
from .serializers import (ExpenseCategorySerializer, FieldExpenseSerializer,
                          ParcelProfitabilitySerializer)


class ExpenseCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExpenseCategory.objects.filter(is_active=True)
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]


class FieldExpenseViewSet(viewsets.ModelViewSet):
    queryset = FieldExpense.objects.select_related('parcel', 'campaign', 'category')
    serializer_class = FieldExpenseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        parcel = self.request.query_params.get('parcel')
        campaign = self.request.query_params.get('campaign')
        category = self.request.query_params.get('category')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if parcel:
            queryset = queryset.filter(parcel_id=parcel)
        if campaign:
            queryset = queryset.filter(campaign_id=campaign)
        if category:
            queryset = queryset.filter(category_id=category)
        if date_from:
            queryset = queryset.filter(expense_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(expense_date__lte=date_to)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_parcel(self, request):
        """Gastos por parcela"""
        parcel_id = request.query_params.get('parcel_id')
        if not parcel_id:
            return Response({'error': 'parcel_id es requerido'}, status=400)
        
        expenses = self.queryset.filter(parcel_id=parcel_id)
        summary = {
            'total_expenses': expenses.aggregate(Sum('total_cost'))['total_cost__sum'] or 0,
            'by_category': expenses.values('category__name').annotate(total=Sum('total_cost'))
        }
        return Response(summary)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Resumen de gastos"""
        campaign_id = request.query_params.get('campaign_id')
        queryset = self.queryset
        
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        summary = {
            'total_expenses': queryset.aggregate(Sum('total_cost'))['total_cost__sum'] or 0,
            'by_category': queryset.values('category__name').annotate(total=Sum('total_cost')),
            'count': queryset.count()
        }
        return Response(summary)


class ParcelProfitabilityViewSet(viewsets.ModelViewSet):
    queryset = ParcelProfitability.objects.select_related('parcel', 'campaign')
    serializer_class = ParcelProfitabilitySerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calcular rentabilidad de una parcela"""
        parcel_id = request.data.get('parcel_id')
        campaign_id = request.data.get('campaign_id')
        
        profitability, created = ParcelProfitability.objects.get_or_create(
            parcel_id=parcel_id,
            campaign_id=campaign_id
        )
        
        profitability.calculate_profitability()
        serializer = self.get_serializer(profitability)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def comparative(self, request):
        """Comparativa de rentabilidad"""
        campaign_id = request.query_params.get('campaign_id')
        queryset = self.queryset
        
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        stats = queryset.aggregate(
            avg_roi=Avg('roi'),
            avg_profit_margin=Avg('profit_margin'),
            total_revenue=Sum('total_revenue'),
            total_expenses=Sum('total_expenses')
        )
        return Response(stats)
