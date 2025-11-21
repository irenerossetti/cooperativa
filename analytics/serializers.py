from rest_framework import serializers
from .models import PriceTrend, DemandTrend


class PriceTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceTrend
        fields = ['id', 'product_name', 'date', 'average_price', 'min_price', 'max_price',
                  'volume_traded', 'trend_direction', 'volatility', 'data_source', 'created_at']
        read_only_fields = ['created_at']


class DemandTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandTrend
        fields = ['id', 'product_name', 'date', 'demand_level', 'demand_index',
                  'trend_direction', 'seasonal_factor', 'market_factors', 'created_at']
        read_only_fields = ['created_at']
