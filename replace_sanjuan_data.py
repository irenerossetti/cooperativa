"""
Reemplazar datos viejos de Cooperativa San Juan con los nuevos de Sam
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from partners.models import Partner, Community
from parcels.models import Parcel, Crop, SoilType
from production.models import HarvestedProduct
from campaigns.models import Campaign
from farm_activities.models import FarmActivity, ActivityType
from inventory.models import InventoryItem, InventoryCategory

def replace_data():
    print("🔄 Reemplazando datos en Cooperativa San Juan...")
    
    # Obtener organizaciones
    sam = Organization.objects.filter(name="Sam").first()
    sanjuan = Organization.objects.filter(name="Cooperativa San Juan").first()
    
    if not sam:
        print("❌ No existe organización Sam")
        return
    
    if not sanjuan:
        print("❌ No existe organización Cooperativa San Juan")
        return
    
    print(f"✓ Origen: {sam.name} (ID: {sam.id})")
    print(f"✓ Destino: {sanjuan.name} (ID: {sanjuan.id})")
    
    # Primero eliminar datos viejos de San Juan
    print("\n🗑️  Eliminando datos viejos de Cooperativa San Juan...")
    models_to_clean = [
        (FarmActivity, 'Actividades agrícolas'),
        (HarvestedProduct, 'Productos cosechados'),
        (Campaign, 'Campañas'),
        (Parcel, 'Parcelas'),
        (Partner, 'Socios'),
        (Community, 'Comunidades'),
        (Crop, 'Tipos de cultivo'),
        (SoilType, 'Tipos de suelo'),
        (InventoryItem, 'Items de inventario'),
        (InventoryCategory, 'Categorías inventario'),
        (ActivityType, 'Tipos de actividad'),
    ]
    
    for model, name in models_to_clean:
        count = model.objects.filter(organization=sanjuan).count()
        if count > 0:
            model.objects.filter(organization=sanjuan).delete()
            print(f"  ✓ {name}: {count} registros eliminados")
    
    # Ahora mover datos de Sam a San Juan
    print("\n📦 Moviendo datos nuevos de Sam a Cooperativa San Juan...")
    models_to_move = [
        (SoilType, 'Tipos de suelo'),
        (Community, 'Comunidades'),
        (Partner, 'Socios'),
        (Crop, 'Tipos de cultivo'),
        (Parcel, 'Parcelas'),
        (Campaign, 'Campañas'),
        (HarvestedProduct, 'Productos cosechados'),
        (ActivityType, 'Tipos de actividad'),
        (FarmActivity, 'Actividades agrícolas'),
        (InventoryCategory, 'Categorías inventario'),
        (InventoryItem, 'Items de inventario'),
    ]
    
    total_moved = 0
    for model, name in models_to_move:
        count = model.objects.filter(organization=sam).update(organization=sanjuan)
        if count > 0:
            print(f"  ✓ {name}: {count} registros movidos")
            total_moved += count
    
    print(f"\n✅ Total movido: {total_moved} registros")
    print(f"✓ Todos los datos ahora están en: {sanjuan.name}")
    
    # Eliminar organización Sam
    print(f"\n🗑️  Eliminando organización '{sam.name}'...")
    sam.delete()
    print("✅ Listo!")

if __name__ == '__main__':
    replace_data()
