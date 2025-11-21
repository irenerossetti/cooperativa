from django.contrib import admin
from .models import PaymentMethod, Customer, Order, OrderItem, Payment


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'requires_reference']
    list_filter = ['is_active']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'document_type', 'document_number', 'phone', 'is_active']
    list_filter = ['document_type', 'is_active']
    search_fields = ['name', 'document_number', 'email']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'order_date', 'total', 'status']
    list_filter = ['status', 'order_date']
    search_fields = ['order_number', 'customer__name']
    inlines = [OrderItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'amount', 'payment_date', 'status']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['order__order_number', 'reference_number']
