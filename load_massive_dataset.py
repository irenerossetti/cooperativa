"""
Script para cargar dataset masivo de datos agrícolas
Genera ~2000 registros de producción, parcelas, cosechas, etc.
"""
import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from partners.models import Partner, Community
from parcels.models import Parcel, Crop, SoilType
from production.models import HarvestedProduct
from campaigns.models import Campaign
from farm_activities.models import FarmActivity, ActivityType
from inventory.models import InventoryItem, InventoryCategory
from tenants.models import Organization
from tenants.middleware import set_current_organization
from django.contrib.auth import get_user_model

User = get_user_model()

# Datos realistas para Argentina
CULTIVOS = [
    ('Maíz', 8000, 12000), ('Soja', 3000, 5000), ('Trigo', 4000, 6000),
    ('Girasol', 2500, 4000), ('Cebada', 3500, 5500), ('Sorgo', 4000, 7000),
    ('Avena', 3000, 5000), ('Arroz', 6000, 9000), ('Papa', 25000, 40000),
    ('Tomate', 50000, 80000), ('Cebolla', 30000, 50000), ('Ajo', 8000, 12000)
]

COMUNIDADES = [
    'Pocito', 'Chimbas', 'Rawson', 'Santa Lucía', 'Rivadavia',
    'Caucete', 'Angaco', 'Albardón', 'San Martín', 'Ullum',
    'Zonda', 'Sarmiento', 'Jáchal', 'Valle Fértil', 'Calingasta'
]

TIPOS_SUELO = [
    ('Arcilloso', 'Retiene agua, rico en nutrientes'),
    ('Arenoso', 'Buen drenaje, bajo en nutrientes'),
    ('Limoso', 'Fértil, retiene humedad moderada'),
    ('Franco', 'Balance ideal de arena, limo y arcilla'),
    ('Pedregoso', 'Drenaje excelente, bajo en materia orgánica')
]

ACTIVIDADES = [
    'Siembra', 'Riego', 'Fertilización', 'Control de plagas',
    'Cosecha', 'Poda', 'Preparación del suelo', 'Aplicación de herbicida'
]

def create_bulk_data():
    print("🚀 Iniciando carga masiva de datos...")
    
    # 1. Obtener organización Cooperativa San Juan
    org = Organization.objects.filter(name="Cooperativa San Juan").first()
    if not org:
        print("❌ No existe la organización 'Cooperativa San Juan'")
        return
    print(f"✓ Organización: {org.name}")
    
    # Configurar contexto de organización para evitar errores de auditoría
    set_current_organization(org)
    
    # 2. Crear tipos de suelo (5 registros)
    soil_types = []
    for nombre, desc in TIPOS_SUELO:
        soil, _ = SoilType.objects.get_or_create(
            name=nombre,
            organization=org,
            defaults={'description': desc}
        )
        soil_types.append(soil)
    print(f"✓ Tipos de suelo: {len(soil_types)}")
    
    # 3. Crear comunidades (15 registros)
    communities = []
    for i, nombre in enumerate(COMUNIDADES):
        comm, _ = Community.objects.get_or_create(
            name=nombre,
            organization=org,
            defaults={
                'description': f'Comunidad de {nombre}, San Juan, Argentina',
                'is_active': True
            }
        )
        communities.append(comm)
    print(f"✓ Comunidades: {len(communities)}")
    
    # 4. Crear socios (100 registros)
    partners = []
    print("Creando socios...")
    for i in range(100):
        partner, _ = Partner.objects.get_or_create(
            ci=f"{2000000 + i}",
            organization=org,
            defaults={
                'nit': f"{100000000 + i}",
                'first_name': f'Socio{i}',
                'last_name': f'Apellido{i}',
                'email': f'socio{i}@coop.com',
                'phone': f'+5492644{100000 + i}',
                'address': f'Calle {i}, San Juan',
                'community': random.choice(communities),
                'status': 'ACTIVE'
            }
        )
        partners.append(partner)
    print(f"✓ Socios: {len(partners)}")
    
    # 5. Crear tipos de cultivo (12 registros)
    crop_types = []
    for cultivo_data in CULTIVOS:
        crop, _ = Crop.objects.get_or_create(
            name=cultivo_data[0],
            organization=org,
            defaults={
                'description': f'Cultivo de {cultivo_data[0]}',
                'is_active': True
            }
        )
        crop_types.append(crop)
    print(f"✓ Tipos de cultivo: {len(crop_types)}")
    
    # 6. Crear parcelas (300 registros)
    parcels = []
    print("Creando parcelas...")
    for i in range(300):
        parcel, _ = Parcel.objects.get_or_create(
            code=f"P{i:04d}",
            organization=org,
            defaults={
                'name': f'Parcela {i}',
                'surface': Decimal(random.uniform(0.5, 5.0)),
                'soil_type': random.choice(soil_types),
                'partner': random.choice(partners),
                'location': f'Lote {i//10 + 1}, San Juan',
                'current_crop': random.choice(crop_types) if i % 3 != 0 else None,
                'status': 'ACTIVE'
            }
        )
        parcels.append(parcel)
    print(f"✓ Parcelas: {len(parcels)}")
    
    # 7. Crear campañas (20 registros - últimos 5 años)
    campaigns = []
    base_year = 2020
    for year in range(base_year, base_year + 5):
        for i, season in enumerate(['Verano', 'Otoño', 'Invierno', 'Primavera']):
            start = datetime(year, [1,4,7,10][i], 1)
            camp, _ = Campaign.objects.get_or_create(
                code=f'C{year}{i+1:02d}',
                organization=org,
                defaults={
                    'name': f'{season} {year}',
                    'description': f'Campaña de {season} {year}',
                    'start_date': start.date(),
                    'end_date': (start + timedelta(days=90)).date(),
                    'target_area': Decimal(random.randint(100, 500)),
                    'target_production': Decimal(random.randint(50000, 200000)),
                    'status': 'ACTIVE' if year == 2025 else 'COMPLETED'
                }
            )
            campaigns.append(camp)
    print(f"✓ Campañas: {len(campaigns)}")
    

    
    # 8. Crear productos cosechados (800 registros)
    print("Creando productos cosechados...")
    harvested = []
    for i in range(800):
        parcel = random.choice(parcels)
        campaign = random.choice(campaigns)
        cultivo_data = random.choice(CULTIVOS)
        
        harvest, _ = HarvestedProduct.objects.get_or_create(
            campaign=campaign,
            parcel=parcel,
            partner=parcel.partner,
            product_name=cultivo_data[0],
            harvest_date=(datetime.now() - timedelta(days=random.randint(0, 365))).date(),
            organization=org,
            defaults={
                'quantity': Decimal(random.uniform(cultivo_data[1], cultivo_data[2])),
                'quality_grade': random.choice(['A', 'B', 'C']),
                'moisture_percentage': Decimal(random.uniform(10, 20)),
                'temperature': Decimal(random.uniform(15, 25)),
                'storage_location': f'Depósito {random.randint(1, 5)}',
                'observations': f'Cosecha {i}'
            }
        )
        harvested.append(harvest)
    print(f"✓ Productos cosechados: {len(harvested)}")
    
    # 9. Crear tipos de actividad
    activity_types = []
    type_mapping = {
        'Siembra': 'SOWING',
        'Riego': 'IRRIGATION',
        'Fertilización': 'FERTILIZATION',
        'Control de plagas': 'PEST_CONTROL',
        'Cosecha': 'HARVEST'
    }
    for act_name in ['Siembra', 'Riego', 'Fertilización', 'Control de plagas', 'Cosecha']:
        act_type, _ = ActivityType.objects.get_or_create(
            name=type_mapping[act_name],
            organization=org,
            defaults={'description': f'Actividad de {act_name.lower()}', 'is_active': True}
        )
        activity_types.append(act_type)
    print(f"✓ Tipos de actividad: {len(activity_types)}")
    
    # 10. Crear actividades agrícolas (400 registros)
    print("Creando actividades agrícolas...")
    for i in range(400):
        parcel = random.choice(parcels)
        campaign = random.choice(campaigns)
        scheduled = (datetime.now() - timedelta(days=random.randint(0, 180))).date()
        
        FarmActivity.objects.get_or_create(
            activity_type=random.choice(activity_types),
            campaign=campaign,
            parcel=parcel,
            scheduled_date=scheduled,
            organization=org,
            defaults={
                'actual_date': scheduled if i % 3 != 0 else None,
                'description': f'Actividad {i} en {parcel.name}',
                'quantity': Decimal(random.uniform(10, 500)),
                'area_covered': parcel.surface,
                'workers_count': random.randint(1, 5),
                'hours_worked': Decimal(random.uniform(2, 8)),
                'status': random.choice(['PENDING', 'COMPLETED', 'IN_PROGRESS']),
                'observations': f'Observación {i}'
            }
        )
    print(f"✓ Actividades agrícolas: 400")
    
    # 11. Crear categorías de inventario
    categories = []
    cat_mapping = {
        'Semillas': 'SEED',
        'Fertilizantes': 'FERTILIZER',
        'Pesticidas': 'PESTICIDE',
        'Herramientas': 'TOOL'
    }
    for cat_name, cat_code in cat_mapping.items():
        cat, _ = InventoryCategory.objects.get_or_create(
            name=cat_code,
            organization=org,
            defaults={'description': f'Categoría de {cat_name}', 'is_active': True}
        )
        categories.append(cat)
    print(f"✓ Categorías inventario: {len(categories)}")
    
    # 12. Crear items de inventario (200 registros)
    print("Creando items de inventario...")
    for i in range(200):
        cat = random.choice(categories)
        InventoryItem.objects.get_or_create(
            code=f'INV{i:04d}',
            organization=org,
            defaults={
                'name': f'Item {i}',
                'category': cat,
                'unit_of_measure': random.choice(['kg', 'litros', 'unidades', 'bolsas']),
                'current_stock': Decimal(random.randint(10, 1000)),
                'minimum_stock': Decimal(random.randint(5, 50)),
                'maximum_stock': Decimal(random.randint(500, 2000)),
                'unit_price': Decimal(random.uniform(100, 5000)),
                'is_active': True
            }
        )
    print(f"✓ Items de inventario: 200")
    
    print("\n" + "="*60)
    print("✅ CARGA MASIVA COMPLETADA")
    print("="*60)
    print(f"Total aproximado de registros: ~2000+")
    print(f"- Socios: 100")
    print(f"- Parcelas: 300")
    print(f"- Cultivos: 500")
    print(f"- Productos cosechados: 800")
    print(f"- Actividades: 400")
    print(f"- Inventario: 200")
    print(f"- Comunidades: 15")
    print(f"- Campañas: 20")
    print("="*60)

if __name__ == '__main__':
    create_bulk_data()
