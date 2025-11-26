from rest_framework import serializers
from .models import MarketPrice, PriceAlert


class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = ['id', 'product_type', 'price_per_kg', 'date', 'source']


class PriceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlert
        fields = ['id', 'product_type', 'alert_type', 'message', 
                  'percentage_change', 'is_active', 'created_at']
