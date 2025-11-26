import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import InventoryItem, InventoryCategory

print("=" * 60)
print("CREANDO PRODUCTOS DE CATÁLOGO")
print("=" * 60)

# Crear categorías si no existen
categories = {
    'SEED': InventoryCategory.objects.get_or_create(
        name='SEED',
        defaults={'description': 'Semillas para siembra'}
    )[0],
    'FERTILIZER': InventoryCategory.objects.get_or_create(
        name='FERTILIZER',
        defaults={'description': 'Fertilizantes y abonos'}
    )[0],
}

print("\n✅ Categorías creadas/verificadas")

# Productos del catálogo
productos = [
    {
        'code': 'SEM-MAIZ-001',
        'name': 'Semillas de Maíz Premium',
        'category': 'SEED',
        'quantity': 500.00,
        'unit': 'kg',
        'unit_price': 250.00,
        'description': 'Semillas certificadas de alta calidad'
    },
    {
        'code': 'SEM-QUIN-001',
        'name': 'Semillas de Quinua Orgánica',
        'category': 'SEED',
        'quantity': 200.00,
        'unit': 'kg',
        'unit_price': 320.00,
        'description': 'Variedad orgánica certificada'
    },
    {
        'code': 'SEM-TRIG-001',
        'name': 'Semillas de Trigo',
        'category': 'SEED',
        'quantity': 350.00,
        'unit': 'kg',
        'unit_price': 180.00,
        'description': 'Ideal para clima templado'
    },
    {
        'code': 'SEM-SOYA-001',
        'name': 'Semillas de Soya',
        'category': 'SEED',
        'quantity': 400.00,
        'unit': 'kg',
        'unit_price': 220.00,
        'description': 'Alto rendimiento'
    },
    {
        'code': 'FERT-ORG-001',
        'name': 'Fertilizante Orgánico',
        'category': 'FERTILIZER',
        'quantity': 600.00,
        'unit': 'kg',
        'unit_price': 180.00,
        'description': 'Fertilizante 100% orgánico'
    },
    {
        'code': 'FERT-NPK-001',
        'name': 'Fertilizante NPK 15-15-15',
        'category': 'FERTILIZER',
        'quantity': 450.00,
        'unit': 'kg',
        'unit_price': 220.00,
        'description': 'Nutrición balanceada'
    },
    {
        'code': 'FERT-COMP-001',
        'name': 'Compost Premium',
        'category': 'FERTILIZER',
        'quantity': 300.00,
        'unit': 'kg',
        'unit_price': 150.00,
        'description': 'Mejora la estructura del suelo'
    },
    {
        'code': 'FERT-HUM-001',
        'name': 'Humus de Lombriz',
        'category': 'FERTILIZER',
        'quantity': 250.00,
        'unit': 'kg',
        'unit_price': 200.00,
        'description': 'Rico en nutrientes'
    },
]

print("\n📦 Creando productos del catálogo...")
created_count = 0
updated_count = 0

for producto_data in productos:
    try:
        category = categories[producto_data['category']]
        
        # Verificar si ya existe
        existing = InventoryItem.objects.filter(
            name=producto_data['name']
        ).first()
        
        if existing:
            # Actualizar
            existing.current_stock = producto_data['quantity']
            existing.unit_price = producto_data['unit_price']
            existing.description = producto_data['description']
            existing.save()
            print(f"ℹ️  Actualizado: {producto_data['name']} - Bs. {producto_data['unit_price']}")
            updated_count += 1
        else:
            # Crear nuevo
            InventoryItem.objects.create(
                code=producto_data['code'],
                name=producto_data['name'],
                category=category,
                current_stock=producto_data['quantity'],
                unit_of_measure=producto_data['unit'],
                unit_price=producto_data['unit_price'],
                minimum_stock=10.00,
                maximum_stock=1000.00,
                description=producto_data['description'],
                is_active=True
            )
            print(f"✅ Creado: {producto_data['name']} - Bs. {producto_data['unit_price']}")
            created_count += 1
            
    except Exception as e:
        print(f"❌ Error con {producto_data['name']}: {e}")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"✅ Productos creados: {created_count}")
print(f"ℹ️  Productos actualizados: {updated_count}")
print(f"📦 Total de productos en inventario: {InventoryItem.objects.count()}")
print("\n🎉 ¡Productos del catálogo listos!")
print("=" * 60)
