"""
Crear items de inventario con stock bajo para probar alertas
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import InventoryItem, InventoryCategory
from tenants.models import Organization

# Obtener organización
org = Organization.objects.first()
print(f"Organización: {org.name}\n")

# Crear o obtener categoría
category, _ = InventoryCategory.objects.get_or_create(
    name=InventoryCategory.FERTILIZER,
    organization=org,
    defaults={"description": "Insumos para producción agrícola"}
)
print(f"Categoría: {category.get_name_display()}\n")

# Crear items con stock bajo
items_data = [
    {"name": "Fertilizante NPK", "current_stock": 5, "minimum_stock": 50, "unit": "kg"},
    {"name": "Semillas de Maíz", "current_stock": 2, "minimum_stock": 20, "unit": "kg"},
    {"name": "Pesticida Orgánico", "current_stock": 15, "minimum_stock": 30, "unit": "litros"},
    {"name": "Herramientas de Cosecha", "current_stock": 3, "minimum_stock": 10, "unit": "unidades"},
]

print("📦 Creando items de inventario con stock bajo...\n")

for data in items_data:
    item, created = InventoryItem.objects.get_or_create(
        name=data["name"],
        organization=org,
        defaults={
            "current_stock": data["current_stock"],
            "minimum_stock": data["minimum_stock"],
            "maximum_stock": data["minimum_stock"] * 3,
            "unit_of_measure": data["unit"],
            "unit_price": 10.0,
            "code": f"INV-{data['name'][:3].upper()}",
            "category": category,
        }
    )
    
    if not created:
        item.current_stock = data["current_stock"]
        item.minimum_stock = data["minimum_stock"]
        item.save()
    
    status = "✅ Creado" if created else "🔄 Actualizado"
    print(f"{status}: {item.name}")
    print(f"   Stock: {item.current_stock} {item.unit_of_measure} (mínimo: {item.minimum_stock})")
    print()

print("✅ Items creados exitosamente!")
