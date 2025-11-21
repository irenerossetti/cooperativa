from rest_framework import serializers
from .models import ExpenseCategory, FieldExpense, ParcelProfitability


class ExpenseCategorySerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'name_display', 'description', 'is_active']


class FieldExpenseSerializer(serializers.ModelSerializer):
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    category_name = serializers.CharField(source='category.get_name_display', read_only=True)
    
    class Meta:
        model = FieldExpense
        fields = ['id', 'parcel', 'parcel_code', 'campaign', 'campaign_name', 'category',
                  'category_name', 'description', 'expense_date', 'quantity', 'unit_cost',
                  'total_cost', 'farm_activity', 'inventory_item', 'notes', 'created_at']
        read_only_fields = ['total_cost', 'created_at']


class ParcelProfitabilitySerializer(serializers.ModelSerializer):
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    
    class Meta:
        model = ParcelProfitability
        fields = ['id', 'parcel', 'parcel_code', 'campaign', 'campaign_name', 'total_revenue',
                  'total_production', 'average_price', 'total_expenses', 'seed_costs',
                  'fertilizer_costs', 'pesticide_costs', 'labor_costs', 'other_costs',
                  'gross_profit', 'profit_margin', 'roi', 'cost_per_hectare',
                  'revenue_per_hectare', 'yield_per_hectare', 'calculated_at', 'notes']
        read_only_fields = ['calculated_at']
