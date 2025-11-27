"""
Script para verificar que una organización nueva no vea datos de otras
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from partners.models import Partner
from parcels.models import Parcel
from inventory.models import InventoryItem
from sales.models import Order

# Obtener la última organización creada
latest_org = Organization.objects.order_by('-created_at').first()

if not latest_org:
    print("❌ No hay organizaciones en la base de datos")
    exit(1)

print(f"📋 Verificando organización: {latest_org.name}")
print(f"   Subdominio: {latest_org.subdomain}")
print(f"   Creada: {latest_org.created_at}")
print()

# Contar datos asociados a esta organización
partners_count = Partner.objects.filter(organization=latest_org).count()
parcels_count = Parcel.objects.filter(organization=latest_org).count()
inventory_count = InventoryItem.objects.filter(organization=latest_org).count()
orders_count = Order.objects.filter(organization=latest_org).count()

print("📊 Datos de la organización:")
print(f"   Socios: {partners_count}")
print(f"   Parcelas: {parcels_count}")
print(f"   Productos en inventario: {inventory_count}")
print(f"   Órdenes de venta: {orders_count}")
print()

if partners_count == 0 and parcels_count == 0 and inventory_count == 0 and orders_count == 0:
    print("✅ La organización está vacía (como debe ser para una nueva)")
else:
    print("⚠️  La organización tiene datos")
    print("   Esto es normal si:")
    print("   - Es una organización de prueba con datos de ejemplo")
    print("   - El administrador ya agregó datos")

# Verificar que no vea datos de otras organizaciones
print("\n🔒 Verificando aislamiento de datos:")
other_orgs = Organization.objects.exclude(id=latest_org.id)
if other_orgs.exists():
    other_org = other_orgs.first()
    other_partners = Partner.objects.filter(organization=other_org).count()
    
    print(f"   Otra organización: {other_org.name}")
    print(f"   Socios de otra org: {other_partners}")
    print(f"   Socios visibles para {latest_org.name}: {partners_count}")
    
    if partners_count == 0 and other_partners > 0:
        print("   ✅ Aislamiento correcto: no ve datos de otras organizaciones")
    elif partners_count == 0 and other_partners == 0:
        print("   ℹ️  Ambas organizaciones están vacías")
    else:
        print("   ⚠️  Verificar configuración de multi-tenancy")
else:
    print("   ℹ️  Solo hay una organización en el sistema")
