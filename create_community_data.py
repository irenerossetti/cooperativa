"""
Script para crear datos de prueba de comunidades y asociar socios
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from partners.models import Partner, Community
from parcels.models import Parcel
from production.models import HarvestedProduct
from campaigns.models import Campaign
from django.utils import timezone
import random

def create_communities():
    """Crear comunidades de prueba"""
    from tenants.models import Organization
    
    # Obtener la primera organización
    org = Organization.objects.first()
    if not org:
        print("⚠️  No hay organizaciones. Creando una organización de prueba...")
        org = Organization.objects.create(
            name='Cooperativa Demo',
            slug='cooperativa-demo',
            is_active=True
        )
        print(f"✅ Organización creada: {org.name}")
    
    communities_data = [
        {'name': 'San Juan', 'description': 'Comunidad San Juan'},
        {'name': 'El Progreso', 'description': 'Comunidad El Progreso'},
        {'name': 'La Esperanza', 'description': 'Comunidad La Esperanza'},
        {'name': 'Villa Nueva', 'description': 'Comunidad Villa Nueva'},
        {'name': 'Santa Rosa', 'description': 'Comunidad Santa Rosa'},
    ]
    
    communities = []
    for comm_data in communities_data:
        community, created = Community.objects.get_or_create(
            organization=org,
            name=comm_data['name'],
            defaults={'description': comm_data['description']}
        )
        communities.append(community)
        if created:
            print(f"✅ Comunidad creada: {community.name}")
        else:
            print(f"ℹ️  Comunidad ya existe: {community.name}")
    
    return communities

def assign_partners_to_communities(communities):
    """Asignar socios a comunidades"""
    partners = Partner.objects.all()
    
    if not partners.exists():
        print("⚠️  No hay socios en la base de datos")
        return
    
    for partner in partners:
        # Asignar comunidad aleatoria si no tiene
        if not partner.community:
            partner.community = random.choice(communities)
            partner.save()
            print(f"✅ Socio {partner.first_name} {partner.last_name} asignado a {partner.community.name}")

def create_production_data():
    """Crear datos de producción para los socios"""
    from tenants.models import Organization
    
    # Obtener organización
    org = Organization.objects.first()
    if not org:
        print("⚠️  No hay organizaciones")
        return
    
    partners = Partner.objects.all()
    
    # Nombres de productos
    product_names = ['Papa', 'Quinua', 'Maíz', 'Trigo', 'Cebada']
    
    # Obtener campañas existentes
    campaigns = list(Campaign.objects.all())
    if not campaigns:
        print("⚠️  No hay campañas. Creando una campaña de prueba...")
        campaign = Campaign.objects.create(
            organization=org,
            name='Campaña 2024',
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            status='ACTIVE'
        )
        campaigns = [campaign]
    
    # Crear producción para cada socio
    for partner in partners:
        parcels = partner.parcels.all()
        
        if not parcels.exists():
            print(f"⚠️  Socio {partner.first_name} {partner.last_name} no tiene parcelas")
            continue
        
        for parcel in parcels:
            # Crear 2-3 registros de producción por parcela
            for _ in range(random.randint(2, 3)):
                product_name = random.choice(product_names)
                quantity = random.uniform(500, 3000)
                campaign = random.choice(campaigns)
                
                harvested = HarvestedProduct(
                    organization=org,
                    partner=partner,
                    parcel=parcel,
                    campaign=campaign,
                    product_name=product_name,
                    quantity=quantity,
                    harvest_date=timezone.now().date(),
                    quality_grade='BUENA'
                )
                harvested.save()
        
        print(f"✅ Producción creada para {partner.first_name} {partner.last_name}")

def main():
    print("🚀 Iniciando creación de datos de comunidades...\n")
    
    # Crear comunidades
    print("1️⃣ Creando comunidades...")
    communities = create_communities()
    print(f"\n✅ Total comunidades: {len(communities)}\n")
    
    # Asignar socios a comunidades
    print("2️⃣ Asignando socios a comunidades...")
    assign_partners_to_communities(communities)
    print()
    
    # Crear datos de producción
    print("3️⃣ Creando datos de producción...")
    create_production_data()
    print()
    
    # Resumen
    print("\n" + "="*50)
    print("📊 RESUMEN")
    print("="*50)
    print(f"Comunidades: {Community.objects.count()}")
    print(f"Socios: {Partner.objects.count()}")
    print(f"Socios con comunidad: {Partner.objects.exclude(community=None).count()}")
    print(f"Parcelas: {Parcel.objects.count()}")
    print(f"Productos cosechados: {HarvestedProduct.objects.count()}")
    print("="*50)
    print("\n✅ ¡Datos creados exitosamente!")

if __name__ == '__main__':
    main()
