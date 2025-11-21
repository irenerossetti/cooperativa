from rest_framework import serializers
from .models import PriceList, PriceListItem


class PriceListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceListItem
        fields = ['id', 'product_name', 'unit_price', 'unit_of_measure', 
                  'min_quantity', 'discount_percentage', 'notes', 'is_active']


class PriceListSerializer(serializers.ModelSerializer):
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    items = PriceListItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = PriceList
        fields = ['id', 'name', 'code', 'campaign', 'campaign_name', 'start_date', 
                  'end_date', 'is_active', 'description', 'items', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_code(self, value):
        price_list_id = self.instance.id if self.instance else None
        if PriceList.objects.filter(code=value).exclude(id=price_list_id).exists():
            raise serializers.ValidationError("Este código ya está registrado.")
        return value

    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError({
                    "end_date": "La fecha de fin debe ser posterior a la fecha de inicio."
                })
        return data
