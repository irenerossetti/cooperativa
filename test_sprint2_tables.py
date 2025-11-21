"""
Script para verificar las tablas del Sprint 2
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from campaigns.models import Campaign
from farm_activities.models import FarmActivity, ActivityType
from inventory.models import InventoryItem, InventoryMovement, InventoryCategory, StockAlert
from production.models import HarvestedProduct

def test_sprint2_tables():
    print("🔍 Verificando tablas del Sprint 2...\n")
    
    print("📊 SPRINT 2 - Tablas y Registros:")
    print("="*60)
    
    # Campañas
    print("\n🎯 CAMPAÑAS:")
    print(f"   Campañas: {Campaign.objects.count()}")
    
    # Labores Agrícolas
    print("\n🌾 LABORES AGRÍCOLAS:")
    print(f"   Tipos de Labor: {ActivityType.objects.count()}")
    print(f"   Labores Registradas: {FarmActivity.objects.count()}")
    
    print("\n   Tipos de labor disponibles:")
    for activity_type in ActivityType.objects.all():
        print(f"      - {activity_type.get_name_display()}")
    
    # Inventario
    print("\n📦 INVENTARIO:")
    print(f"   Categorías: {InventoryCategory.objects.count()}")
    print(f"   Items: {InventoryItem.objects.count()}")
    print(f"   Movimientos: {InventoryMovement.objects.count()}")
    print(f"   Alertas de Stock: {StockAlert.objects.count()}")
    
    print("\n   Categorías de inventario:")
    for category in InventoryCategory.objects.all():
        print(f"      - {category.get_name_display()}: {category.description}")
    
    # Producción
    print("\n🌽 PRODUCCIÓN:")
    print(f"   Productos Cosechados: {HarvestedProduct.objects.count()}")
    
    print("\n" + "="*60)
    print("✅ Todas las tablas del Sprint 2 están creadas correctamente")
    print("🎉 Base de datos lista para usar!\n")
    
    # Mostrar estructura de tablas
    from django.db import connection
    print("📋 ESTRUCTURA DE TABLAS DEL SPRINT 2:")
    print("="*60)
    
    tables_sprint2 = [
        'campaigns',
        'campaigns_parcels', 
        'campaigns_partners',
        'activity_types',
        'farm_activities',
        'inventory_categories',
        'inventory_items',
        'inventory_movements',
        'stock_alerts',
        'harvested_products'
    ]
    
    with connection.cursor() as cursor:
        for table in tables_sprint2:
            cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table}'
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            print(f"\n📄 Tabla: {table}")
            print(f"   Columnas: {len(columns)}")
            for col_name, col_type in columns[:5]:  # Mostrar solo las primeras 5
                print(f"      - {col_name}: {col_type}")
            if len(columns) > 5:
                print(f"      ... y {len(columns) - 5} columnas más")

if __name__ == "__main__":
    test_sprint2_tables()
