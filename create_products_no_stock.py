import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from production.models import HarvestedProduct
from campaigns.models import Campaign
from parcels.models import Parcel
from partners.models import Partner

print("=" * 60)
print("CREANDO PRODUCTOS SIN STOCK (AGOTADOS)")
print("=" * 60)

# Obtener datos necesarios
try:
    campaign = Campaign.objects.filter(status='ACTIVE').first()
    if not campaign:
        print("❌ No hay campañas activas")
        exit(1)
    print(f"✅ Usando campaña: {campaign.name}")

    partner = Partner.objects.first()
    if not partner:
        print("❌ No hay socios")
        exit(1)
    print(f"✅ Usando socio: {partner.full_name}")

    parcel = Parcel.objects.filter(partner=partner).first()
    if not parcel:
        print("❌ No hay parcelas")
        exit(1)
    print(f"✅ Usando parcela: {parcel.code}")

except Exception as e:
    print(f"❌ Error obteniendo datos: {e}")
    exit(1)

# Productos SIN STOCK (agotados)
productos_sin_stock = [
    {
        'product_name': 'Semillas de Arroz (AGOTADO)',
        'quantity': 0.00,
        'quality_grade': 'A',
        'description': 'Stock agotado - Producto no disponible'
    },
    {
        'product_name': 'Semillas de Girasol (AGOTADO)',
        'quantity': 0.00,
        'quality_grade': 'B+',
        'description': 'Stock agotado - Próxima cosecha en 2 meses'
    },
    {
        'product_name': 'Semillas de Avena (AGOTADO)',
        'quantity': 0.00,
        'quality_grade': 'A',
        'description': 'Stock agotado - Reposición pendiente'
    },
]

print("\n📦 Creando productos sin stock...")
created_count = 0

for producto_data in productos_sin_stock:
    try:
        # Verificar si ya existe
        existing = HarvestedProduct.objects.filter(
            product_name=producto_data['product_name'],
            campaign=campaign
        ).first()
        
        if existing:
            # Actualizar a stock 0
            existing.quantity = 0.00
            existing.observations = producto_data['description']
            existing.save()
            print(f"ℹ️  Actualizado a stock 0: {producto_data['product_name']}")
        else:
            # Crear nuevo con stock 0
            HarvestedProduct.objects.create(
                campaign=campaign,
                parcel=parcel,
                partner=partner,
                product_name=producto_data['product_name'],
                harvest_date=date.today() - timedelta(days=30),
                quantity=0.00,
                quality_grade=producto_data['quality_grade'],
                moisture_percentage=12.5,
                temperature=20.0,
                storage_location='Almacén Principal',
                observations=producto_data['description']
            )
            print(f"✅ Creado sin stock: {producto_data['product_name']}")
            created_count += 1
            
    except Exception as e:
        print(f"❌ Error con {producto_data['product_name']}: {e}")

# También vamos a reducir el stock de algunos productos existentes
print("\n📉 Reduciendo stock de algunos productos existentes...")
productos_a_reducir = [
    {'nombre': 'Semillas de Soya', 'nuevo_stock': 5.00},
    {'nombre': 'Cebada', 'nuevo_stock': 10.00},
]

for item in productos_a_reducir:
    try:
        producto = HarvestedProduct.objects.filter(
            product_name__icontains=item['nombre']
        ).first()
        
        if producto:
            producto.quantity = item['nuevo_stock']
            producto.save()
            print(f"✅ {producto.product_name}: Stock reducido a {item['nuevo_stock']} kg")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"✅ Productos sin stock creados: {created_count}")
print(f"📦 Total de productos: {HarvestedProduct.objects.count()}")
print(f"❌ Productos con stock 0: {HarvestedProduct.objects.filter(quantity=0).count()}")
print(f"⚠️  Productos con stock bajo (<20): {HarvestedProduct.objects.filter(quantity__lt=20, quantity__gt=0).count()}")
print("\n🎉 ¡Productos de prueba listos!")
print("=" * 60)
