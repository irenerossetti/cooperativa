from rest_framework import serializers
from .models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    customer_name = serializers.CharField(source='order.customer.name', read_only=True)
    community_name = serializers.CharField(source='destination_community.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Shipment
        fields = ['id', 'shipment_number', 'order', 'order_number', 'customer_name',
                  'destination_community', 'community_name', 'destination_address',
                  'scheduled_date', 'actual_delivery_date', 'carrier', 'vehicle_plate',
                  'driver_name', 'driver_phone', 'status', 'status_display',
                  'tracking_number', 'notes', 'received_by', 'signature',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_shipment_number(self, value):
        shipment_id = self.instance.id if self.instance else None
        if Shipment.objects.filter(shipment_number=value).exclude(id=shipment_id).exists():
            raise serializers.ValidationError("Este número de envío ya existe.")
        return value
