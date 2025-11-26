import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sales.models import Customer, Order, OrderItem
from production.models import HarvestedProduct
from campaigns.models import Campaign
from partners.models import Partner

print("=" * 60)
print("CREANDO DATOS DE PRUEBA PARA VENTAS")
print("=" * 60)

# Crear clientes
print("\n👥 Creando clientes...")
clientes_data = [
    {
        'name': 'Juan Pérez García',
        'document_type': 'CI',
        'document_number': '7654321',
        'email': 'juan.perez@email.com',
        'phone': '70123456',
        'address': 'Av. Principal #123, La Paz'
    },
    {
        'name': 'María López Mamani',
        'document_type': 'CI',
        'document_number': '8765432',
        'email': 'maria.lopez@email.com',
        'phone': '71234567',
        'address': 'Calle Comercio #456, El Alto'
    },
    {
        'name': 'Empresa Agrícola S.R.L.',
        'document_type': 'NIT',
        'document_number': '1234567890',
        'email': 'ventas@empresaagricola.com',
        'phone': '72345678',
        'address': 'Zona Industrial, Santa Cruz'
    },
]

for cliente_data in clientes_data:
    cliente, created = Customer.objects.get_or_create(
        document_number=cliente_data['document_number'],
        defaults=cliente_data
    )
    if created:
        print(f"✅ Cliente creado: {cliente.name}")
    else:
        print(f"ℹ️  Cliente ya existe: {cliente.name}")

# Obtener datos necesarios
campaign = Campaign.objects.filter(status='ACTIVE').first()
if not campaign:
    print("❌ No hay campañas activas")
    exit(1)

productos = list(HarvestedProduct.objects.all()[:5])
if not productos:
    print("❌ No hay productos cosechados")
    exit(1)

clientes = list(Customer.objects.all())

# Crear pedidos de ejemplo
print("\n📦 Creando pedidos de ejemplo...")

import random

# Generar 15 pedidos con datos variados
pedidos_data = []
estados = ['DRAFT', 'CONFIRMED', 'PAID', 'SHIPPED', 'DELIVERED', 'CANCELLED']
dias_atras = [0, 1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 35, 40, 45, 50]

for i in range(15):
    # Seleccionar cliente aleatorio
    cliente = random.choice(clientes)
    
    # Seleccionar estado (más pedidos confirmados y entregados)
    if i < 3:
        estado = 'DRAFT'
    elif i < 6:
        estado = 'CONFIRMED'
    elif i < 9:
        estado = 'DELIVERED'
    elif i < 12:
        estado = 'PAID'
    elif i < 14:
        estado = 'SHIPPED'
    else:
        estado = 'CANCELLED'
    
    # Crear items aleatorios (1-3 productos por pedido)
    num_items = random.randint(1, 3)
    items = []
    productos_usados = []
    
    for _ in range(num_items):
        # Seleccionar producto que no se haya usado en este pedido
        producto_disponible = [p for p in productos if p not in productos_usados]
        if not producto_disponible:
            break
        
        producto = random.choice(producto_disponible)
        productos_usados.append(producto)
        
        items.append({
            'product': producto,
            'quantity': random.randint(10, 200),
            'unit_price': random.choice([200, 220, 250, 280, 300, 320, 350])
        })
    
    pedidos_data.append({
        'customer': cliente,
        'status': estado,
        'items': items,
        'dias_atras': dias_atras[i]
    })

created_orders = 0
for i, pedido_data in enumerate(pedidos_data):
    try:
        # Generar número de pedido único
        fecha_pedido = date.today() - timedelta(days=pedido_data['dias_atras'])
        order_number = f"ORD-{fecha_pedido.strftime('%Y%m%d')}-{i+1:03d}"
        
        # Verificar si ya existe
        if Order.objects.filter(order_number=order_number).exists():
            print(f"ℹ️  Pedido ya existe: {order_number}")
            continue
        
        # Crear pedido
        order = Order.objects.create(
            order_number=order_number,
            customer=pedido_data['customer'],
            campaign=campaign,
            order_date=fecha_pedido,
            delivery_date=fecha_pedido + timedelta(days=random.randint(3, 10)) if pedido_data['status'] != 'CANCELLED' else None,
            status=pedido_data['status'],
            subtotal=0,
            total=0,
            notes=f"Pedido de prueba #{i+1}" if random.random() > 0.5 else ""
        )
        
        # Crear items
        for item_data in pedido_data['items']:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price']
            )
        
        # Recalcular totales
        order.calculate_totals()
        
        estado_emoji = {
            'DRAFT': '📝',
            'CONFIRMED': '✅',
            'PAID': '💰',
            'SHIPPED': '🚚',
            'DELIVERED': '📦',
            'CANCELLED': '❌'
        }
        
        print(f"{estado_emoji.get(order.status, '📋')} {order.order_number} - {order.customer.name} - Bs. {order.total:.2f} - {order.status}")
        created_orders += 1
        
    except Exception as e:
        print(f"❌ Error creando pedido: {e}")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"✅ Clientes totales: {Customer.objects.count()}")
print(f"✅ Pedidos creados: {created_orders}")
print(f"📦 Total de pedidos: {Order.objects.count()}")
print("\n🎉 ¡Datos de prueba listos!")
print("=" * 60)
