#!/usr/bin/env python
"""
Script para verificar los datos de una organización específica
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from partners.models import Partner
from parcels.models import Parcel
from production.models import HarvestedProduct
from campaigns.models import Campaign

def check_organization_data(subdomain):
    """Verifica los datos de una organización"""
    try:
        org = Organization.objects.get(subdomain=subdomain)
        print(f"\n{'='*60}")
        print(f"ORGANIZACIÓN: {org.name}")
        print(f"Subdominio: {org.subdomain}")
        print(f"Estado: {org.status}")
        print(f"Plan: {org.plan}")
        print(f"{'='*60}\n")
        
        # Contar datos
        partners = Partner.objects.filter(organization=org).count()
        parcels = Parcel.objects.filter(organization=org).count()
        products = HarvestedProduct.objects.filter(organization=org).count()
        campaigns = Campaign.objects.filter(organization=org).count()
        
        print(f"📊 DATOS DE LA ORGANIZACIÓN:")
        print(f"  • Socios: {partners}")
        print(f"  • Parcelas: {parcels}")
        print(f"  • Productos Cosechados: {products}")
        print(f"  • Campañas: {campaigns}")
        print()
        
        if partners == 0 and parcels == 0 and products == 0 and campaigns == 0:
            print("✅ ORGANIZACIÓN VACÍA - Lista para presentación")
        else:
            print("⚠️  ORGANIZACIÓN CON DATOS")
            
    except Organization.DoesNotExist:
        print(f"❌ No se encontró la organización con subdominio: {subdomain}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        subdomain = sys.argv[1]
        check_organization_data(subdomain)
    else:
        print("\n📋 TODAS LAS ORGANIZACIONES:\n")
        orgs = Organization.objects.all().order_by('name')
        for org in orgs:
            partners = Partner.objects.filter(organization=org).count()
            print(f"  • {org.name} ({org.subdomain}): {partners} socios")
        
        print("\n💡 Uso: python check_org_data.py <subdomain>")
        print("   Ejemplo: python check_org_data.py sypha")
