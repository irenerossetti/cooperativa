"""
Crear datos de mercado para probar alertas de precio
"""
import os
import django
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market_analysis.models import MarketPrice
from tenants.models import Organization

# Obtener organización
org = Organization.objects.first()
print(f"Organización: {org.name}\n")

# Crear precios de mercado con variaciones
products_data = [
    {"product": "QUINUA", "current": 8.50, "previous": 7.20, "variation": 18.1},  # Subió mucho
    {"product": "MAIZ", "current": 3.20, "previous": 3.80, "variation": -15.8},   # Bajó mucho
    {"product": "PAPA", "current": 1.80, "previous": 1.75, "variation": 2.9},     # Subió poco
    {"product": "TRIGO", "current": 4.20, "previous": 4.50, "variation": -6.7},   # Bajó moderado
]

print("💰 Creando precios de mercado...\n")

today = date.today()
yesterday = today - timedelta(days=1)

for data in products_data:
    # Eliminar precios anteriores para este producto
    MarketPrice.objects.filter(
        product_type=data["product"],
        organization=org
    ).delete()
    
    # Precio anterior
    MarketPrice.objects.create(
        product_type=data["product"],
        price_per_kg=Decimal(str(data["previous"])),
        organization=org,
        source="Mercado Local"
    )
    
    # Actualizar la fecha manualmente
    old_price = MarketPrice.objects.filter(product_type=data["product"]).first()
    if old_price:
        old_price.date = yesterday
        old_price.save()
    
    # Precio actual
    price = MarketPrice.objects.create(
        product_type=data["product"],
        price_per_kg=Decimal(str(data["current"])),
        organization=org,
        source="Mercado Local"
    )
    
    trend = "📈" if data["variation"] > 0 else "📉"
    print(f"✅ Creado: {data['product']}")
    print(f"   {trend} Bs. {data['current']}/kg (variación: {data['variation']:+.1f}%)")
    print()

print("✅ Precios de mercado creados!")
