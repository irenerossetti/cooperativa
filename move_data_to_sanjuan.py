"""
Mover todos los datos de Sam a San Juan
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

def move_data():
    print("🔄 Moviendo datos de Sam a San Juan...")
    
    # Obtener organizaciones
    sam = Organization.objects.filter(name="Sam").first()
    sanjuan = Organization.objects.filter(name="Cooperativa San Juan").first()
    
    if not sam:
        print("❌ No existe organización Sam")
        return
    
    if not sanjuan:
        print("❌ No existe organización San Juan")
        return
    
    print(f"✓ Origen: {sam.name} (ID: {sam.id})")
    print(f"✓ Destino: {sanjuan.name} (ID: {sanjuan.id})")
    
    # Mover todos los datos
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
            print(f"✓ {name}: {count} registros movidos")
            total_moved += count
    
    print(f"\n✅ Total movido: {total_moved} registros")
    print(f"✓ Todos los datos ahora están en: {sanjuan.name}")
    
    # Opcional: eliminar organización Sam
    print(f"\n¿Eliminar organización '{sam.name}'? (ya no tiene datos)")
    # sam.delete()  # Descomenta si quieres eliminarla

if __name__ == '__main__':
    move_data()
