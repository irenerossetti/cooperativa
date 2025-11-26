"""
Genera datos de producción histórica para entrenar el modelo de ML
"""
import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from parcels.models import Parcel
from production.models import HarvestedProduct
from tenants.middleware import set_current_organization
from tenants.models import Organization

print("Generando datos de producción histórica...")
print("=" * 60)

# Buscar organización con parcelas
org = None
for organization in Organization.objects.all():
    set_current_organization(organization)
    if Parcel.objects.count() > 0:
        org = organization
        break

if not org:
    print("Error: No hay organizaciones con parcelas")
    exit(1)

print(f"Organización: {org.name}")

# Obtener parcelas
parcels = Parcel.objects.all()
print(f"Parcelas disponibles: {parcels.count()}")

if parcels.count() == 0:
    print("Error: No hay parcelas en la base de datos")
    exit(1)

# Generar producción histórica para cada parcela
created_count = 0
for parcel in parcels:
    # Generar entre 2 y 5 registros de producción por parcela
    num_harvests = random.randint(2, 5)
    
    for i in range(num_harvests):
        # Calcular rendimiento base según superficie
        base_yield = 70 + (float(parcel.surface) * 2)  # kg/ha
        
        # Agregar variación aleatoria (-20% a +30%)
        variation = random.uniform(-0.2, 0.3)
        yield_per_ha = base_yield * (1 + variation)
        
        # Calcular cantidad total
        quantity = yield_per_ha * float(parcel.surface)
        
        # Fecha de cosecha (últimos 2 años)
        days_ago = random.randint(30, 730)
        harvest_date = datetime.now().date() - timedelta(days=days_ago)
        
        # Crear registro
        try:
            # Necesitamos una campaña
            from campaigns.models import Campaign
            campaign = Campaign.objects.first()
            if not campaign:
                print("  ⚠️  No hay campañas, creando una...")
                campaign = Campaign.objects.create(
                    name="Campaña 2024",
                    start_date=datetime.now().date() - timedelta(days=365),
                    end_date=datetime.now().date()
                )
            
            product = HarvestedProduct.objects.create(
                campaign=campaign,
                parcel=parcel,
                partner=parcel.partner,
                product_name=f"Cosecha {parcel.current_crop.name if parcel.current_crop else 'General'}",
                quantity=round(quantity, 2),
                harvest_date=harvest_date,
                quality_grade='BUENA' if yield_per_ha > base_yield else 'REGULAR',
                observations=f"Rendimiento: {yield_per_ha:.2f} kg/ha"
            )
            created_count += 1
            print(f"  ✓ {parcel.code}: {quantity:.2f} kg ({yield_per_ha:.2f} kg/ha)")
        except Exception as e:
            print(f"  ✗ Error en {parcel.code}: {e}")

print("\n" + "=" * 60)
print(f"✓ Creados {created_count} registros de producción")
print("=" * 60)
print("\nAhora puedes entrenar el modelo de ML!")
