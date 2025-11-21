from rest_framework import serializers
from .models import InventoryItem, InventoryMovement, InventoryCategory, StockAlert


class InventoryCategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías de inventario"""
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    
    class Meta:
        model = InventoryCategory
        fields = ['id', 'name', 'name_display', 'description', 'is_active', 
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer para items de inventario"""
    category_name = serializers.CharField(source='category.get_name_display', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    stock_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = ['id', 'code', 'name', 'category', 'category_name', 'species', 'variety',
                  'brand', 'germination_percentage', 'unit_of_measure', 'current_stock',
                  'minimum_stock', 'maximum_stock', 'unit_price', 'expiration_date',
                  'is_active', 'is_low_stock', 'stock_status', 'description', 'notes',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'current_stock']

    def validate_code(self, value):
        """Validar que el código no esté duplicado"""
        item_id = self.instance.id if self.instance else None
        if InventoryItem.objects.filter(code=value).exclude(id=item_id).exists():
            raise serializers.ValidationError("Este código ya está registrado.")
        return value


class InventoryMovementSerializer(serializers.ModelSerializer):
    """Serializer para movimientos de inventario"""
    item_name = serializers.CharField(source='item.name', read_only=True)
    movement_type_display = serializers.CharField(source='get_movement_type_display', read_only=True)
    
    class Meta:
        model = InventoryMovement
        fields = ['id', 'item', 'item_name', 'movement_type', 'movement_type_display',
                  'quantity', 'date', 'reference', 'reason', 'unit_cost', 'total_cost',
                  'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        """Validar que haya stock suficiente para salidas"""
        if data.get('movement_type') == InventoryMovement.EXIT:
            item = data.get('item')
            quantity = data.get('quantity')
            if item.current_stock < quantity:
                raise serializers.ValidationError({
                    "quantity": f"Stock insuficiente. Stock actual: {item.current_stock}"
                })
        return data


class StockAlertSerializer(serializers.ModelSerializer):
    """Serializer para alertas de stock"""
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_code = serializers.CharField(source='item.code', read_only=True)
    
    class Meta:
        model = StockAlert
        fields = ['id', 'item', 'item_name', 'item_code', 'alert_date', 'current_stock',
                  'minimum_stock', 'is_resolved', 'resolved_date']
        read_only_fields = ['alert_date']
