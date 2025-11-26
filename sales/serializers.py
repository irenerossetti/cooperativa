from rest_framework import serializers
from .models import PaymentMethod, Customer, Order, OrderItem, Payment


class PaymentMethodSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'name_display', 'description', 'is_active', 
                  'requires_reference', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'document_type', 'document_number', 'email', 'phone',
                  'address', 'partner', 'partner_name', 'is_active', 'notes',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_document_number(self, value):
        customer_id = self.instance.id if self.instance else None
        if Customer.objects.filter(document_number=value).exclude(id=customer_id).exists():
            raise serializers.ValidationError("Este número de documento ya está registrado.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'quantity', 'unit_price', 
                  'line_total', 'notes']
        read_only_fields = ['line_total']


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_quantity = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'customer_name', 'campaign', 'campaign_name',
                  'order_date', 'delivery_date', 'subtotal', 'discount_percentage', 
                  'discount_amount', 'tax_amount', 'total', 'status', 'status_display',
                  'items', 'total_items', 'total_quantity', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'subtotal', 'discount_amount', 'total']

    def validate_order_number(self, value):
        order_id = self.instance.id if self.instance else None
        if Order.objects.filter(order_number=value).exclude(id=order_id).exists():
            raise serializers.ValidationError("Este número de pedido ya existe.")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    payment_method_name = serializers.CharField(source='payment_method.get_name_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_number', 'payment_method', 'payment_method_name',
                  'amount', 'payment_date', 'reference_number', 'receipt_number',
                  'status', 'status_display', 'notes', 'created_at']
        read_only_fields = ['created_at']
