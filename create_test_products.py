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
print("CREANDO PRODUCTOS COSECHADOS DE PRUEBA")
print("=" * 60)

# Obtener datos necesarios
try:
    campaign = Campaign.objects.filter(status='ACTIVE').first()
    if not campaign:
        print("❌ No hay campañas activas. Creando una...")
        campaign = Campaign.objects.create(
            name="Campaña Verano 2024",
            code=f"CAMP-{date.today().year}-001",
            start_date=date.today() - timedelta(days=90),
            end_date=date.today() + timedelta(days=90),
            status='ACTIVE',
            description="Campaña de prueba",
            target_area=100.0,
            target_production=5000.0
        )
        print(f"✅ Campaña creada: {campaign.name}")
    else:
        print(f"✅ Usando campaña: {campaign.name}")

    partner = Partner.objects.first()
    if not partner:
        print("❌ No hay socios. Por favor crea un socio primero.")
        exit(1)
    print(f"✅ Usando socio: {partner.full_name}")

    parcel = Parcel.objects.filter(partner=partner).first()
    if not parcel:
        print("❌ No hay parcelas. Creando una...")
        from parcels.models import SoilType, Crop
        
        soil_type = SoilType.objects.first()
        if not soil_type:
            soil_type = SoilType.objects.create(name="Franco", description="Suelo franco")
        
        crop = Crop.objects.first()
        if not crop:
            crop = Crop.objects.create(name="Maíz", scientific_name="Zea mays")
        
        parcel = Parcel.objects.create(
            code=f"P-{partner.id}-001",
            partner=partner,
            surface=1.5,
            soil_type=soil_type,
            current_crop=crop,
            status='ACTIVE',
            location='Ubicación de prueba'
        )
        print(f"✅ Parcela creada: {parcel.code}")
    else:
        print(f"✅ Usando parcela: {parcel.code}")

except Exception as e:
    print(f"❌ Error obteniendo datos: {e}")
    exit(1)

# Productos a crear
productos = [
    {
        'product_name': 'Semillas de Maíz Premium',
        'quantity': 500.00,
        'quality_grade': 'A',
        'description': 'Semillas certificadas de alta calidad'
    },
    {
        'product_name': 'Semillas de Quinua Orgánica',
        'quantity': 200.00,
        'quality_grade': 'A+',
        'description': 'Variedad orgánica certificada'
    },
    {
        'product_name': 'Semillas de Trigo',
        'quantity': 350.00,
        'quality_grade': 'A',
        'description': 'Ideal para clima templado'
    },
    {
        'product_name': 'Semillas de Soya',
        'quantity': 400.00,
        'quality_grade': 'B+',
        'description': 'Alto rendimiento'
    },
    {
        'product_name': 'Maíz Cosechado',
        'quantity': 500.00,
        'quality_grade': 'A',
        'description': 'Maíz fresco de la última cosecha'
    },
    {
        'product_name': 'Quinua Premium',
        'quantity': 200.00,
        'quality_grade': 'A+',
        'description': 'Quinua de exportación'
    },
    {
        'product_name': 'Trigo Orgánico',
        'quantity': 350.00,
        'quality_grade': 'A',
        'description': 'Trigo orgánico certificado'
    },
    {
        'product_name': 'Cebada',
        'quantity': 280.00,
        'quality_grade': 'B+',
        'description': 'Cebada para cervecería'
    },
]

print("\n📦 Creando productos cosechados...")
created_count = 0
updated_count = 0

for producto_data in productos:
    try:
        # Verificar si ya existe
        existing = HarvestedProduct.objects.filter(
            product_name=producto_data['product_name'],
            campaign=campaign
        ).first()
        
        if existing:
            # Actualizar
            existing.quantity = producto_data['quantity']
            existing.quality_grade = producto_data['quality_grade']
            existing.observations = producto_data['description']
            existing.save()
            print(f"ℹ️  Actualizado: {producto_data['product_name']} - {producto_data['quantity']} kg")
            updated_count += 1
        else:
            # Crear nuevo
            HarvestedProduct.objects.create(
                campaign=campaign,
                parcel=parcel,
                partner=partner,
                product_name=producto_data['product_name'],
                harvest_date=date.today() - timedelta(days=7),
                quantity=producto_data['quantity'],
                quality_grade=producto_data['quality_grade'],
                moisture_percentage=12.5,
                temperature=20.0,
                storage_location='Almacén Principal',
                observations=producto_data['description']
            )
            print(f"✅ Creado: {producto_data['product_name']} - {producto_data['quantity']} kg")
            created_count += 1
            
    except Exception as e:
        print(f"❌ Error con {producto_data['product_name']}: {e}")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"✅ Productos creados: {created_count}")
print(f"ℹ️  Productos actualizados: {updated_count}")
print(f"📦 Total de productos disponibles: {HarvestedProduct.objects.count()}")
print("\n🎉 ¡Productos de prueba listos!")
print("=" * 60)
