#!/usr/bin/env python
"""
Script para agregar fechas de siembra realistas a las parcelas
"""
import os
import sys
import django
from datetime import date, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from parcels.models import Parcel
from tenants.models import Organization
from farm_activities.models import FarmActivity, ActivityType

print("=" * 60)
print("AGREGANDO FECHAS DE SIEMBRA A PARCELAS")
print("=" * 60)

# Obtener organización
org = Organization.objects.filter(subdomain='sammantha').first()
if not org:
    print("ERROR: Organización 'sammantha' no encontrada")
    sys.exit(1)

print(f"\nOrganización: {org.name}")

# Obtener o crear tipo de actividad SOWING
sowing_type, created = ActivityType.objects.get_or_create(
    organization=org,
    name='SOWING',
    defaults={'description': 'Siembra de cultivos'}
)

if created:
    print(f"[OK] Tipo de actividad SOWING creado")
else:
    print(f"[OK] Tipo de actividad SOWING ya existe")

# Obtener parcelas con cultivo
parcels = Parcel.objects.filter(
    organization=org,
    current_crop__isnull=False
)

print(f"\nParcelas con cultivo: {parcels.count()}")

# Días de maduración por cultivo
MATURATION_DAYS = {
    'QUINUA': 150,
    'PAPA': 120,
    'MAIZ': 140,
    'TRIGO': 120,
    'CEBADA': 110,
    'HABA': 100,
    'ARVEJA': 90,
    'ARROZ': 130,
    'SOJA': 120,
    'GIRASOL': 110,
    'SORGO': 100,
    'TOMATE': 90,
    'CEBOLLA': 120,
    'AJO': 150,
    'AVENA': 100,
}

print("\nAgregando fechas de siembra...")

count = 0
for parcel in parcels:
    # Verificar si ya tiene actividad de siembra
    existing = FarmActivity.objects.filter(
        parcel=parcel,
        activity_type=sowing_type
    ).exists()
    
    if existing:
        continue
    
    # Calcular fecha de siembra basada en el cultivo
    crop_name = parcel.current_crop.name.upper()
    expected_days = MATURATION_DAYS.get(crop_name, 120)
    
    # Variar entre 60% y 110% del tiempo de maduración
    days_ago = random.randint(int(expected_days * 0.6), int(expected_days * 1.1))
    planting_date = date.today() - timedelta(days=days_ago)
    
    # Crear actividad de siembra
    try:
        FarmActivity.objects.create(
            organization=org,
            parcel=parcel,
            activity_type=sowing_type,
            scheduled_date=planting_date,
            actual_date=planting_date,
            description=f"Siembra de {parcel.current_crop.name}",
            status='COMPLETED'
        )
        count += 1
        if count <= 5:
            print(f"  [OK] {parcel.code}: {parcel.current_crop.name} - {days_ago} días atrás")
    except Exception as e:
        print(f"  [ERROR] {parcel.code}: {e}")

print(f"\n[OK] {count} actividades de siembra creadas")

print("\n" + "=" * 60)
print("COMPLETADO")
print("=" * 60)
print("\nAhora el widget 'Momento Óptimo Cosecha' debería mostrar")
print("recomendaciones más realistas basadas en fechas de siembra.")
