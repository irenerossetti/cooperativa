import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sales.models import Order, OrderItem, Customer
from production.models import HarvestedProduct
from campaigns.models import Campaign

print("=" * 60)
print("PROBANDO CREACIÓN DE ORDER ITEM")
print("=" * 60)

# Obtener datos necesarios
try:
    # Obtener un producto cosechado
    product = HarvestedProduct.objects.filter(product_name__icontains='semilla').first()
    if not product:
        print("❌ No hay productos cosechados")
        exit(1)
    print(f"✅ Producto: {product.product_name} (ID: {product.id})")
    
    # Obtener un pedido en borrador
    order = Order.objects.filter(status='DRAFT').first()
    if not order:
        print("❌ No hay pedidos en borrador. Creando uno...")
        
        # Obtener o crear cliente
        customer = Customer.objects.first()
        if not customer:
            customer = Customer.objects.create(
                name="Cliente de Prueba",
                document_type="CI",
                document_number="12345678",
                phone="70000000",
                address="Dirección de prueba"
            )
            print(f"✅ Cliente creado: {customer.name}")
        
        # Obtener campaña activa
        campaign = Campaign.objects.filter(status='ACTIVE').first()
        if not campaign:
            print("❌ No hay campañas activas")
            exit(1)
        
        # Crear pedido
        order = Order.objects.create(
            order_number=f"ORD-TEST-{date.today().strftime('%Y%m%d')}",
            customer=customer,
            campaign=campaign,
            order_date=date.today(),
            status='DRAFT'
        )
        print(f"✅ Pedido creado: {order.order_number}")
    else:
        print(f"✅ Pedido: {order.order_number}")
    
    # Intentar crear un OrderItem
    print("\n📦 Creando OrderItem...")
    item_data = {
        'order': order,
        'product': product,
        'quantity': 10.0,
        'unit_price': 250.0
    }
    
    item = OrderItem.objects.create(**item_data)
    print(f"✅ OrderItem creado exitosamente!")
    print(f"   - Producto: {item.product.product_name}")
    print(f"   - Cantidad: {item.quantity}")
    print(f"   - Precio unitario: {item.unit_price}")
    print(f"   - Total línea: {item.line_total}")
    
    print("\n✅ ¡Prueba exitosa!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
