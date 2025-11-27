#!/usr/bin/env python
"""
Script para agregar datos necesarios para el optimizador de cosecha
"""
import os
import sys
import django
from datetime import date, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from parcels.models import Parcel, Crop
from tenants.models import Organization

print("=" * 60)
print("CONFIGURANDO DATOS PARA OPTIMIZADOR DE COSECHA")
print("=" * 60)

# Obtener organización
org = Organization.objects.filter(subdomain='sammantha').first()
if not org:
    print("ERROR: Organización 'sammantha' no encontrada")
    sys.exit(1)

print(f"\nOrganización: {org.name}")

# Verificar si hay cultivos
crops = Crop.objects.filter(organization=org)
print(f"\nCultivos disponibles: {crops.count()}")

if crops.count() == 0:
    print("\nCreando cultivos de ejemplo...")
    crop_names = ['QUINUA', 'PAPA', 'MAIZ', 'TRIGO', 'CEBADA', 'HABA', 'ARVEJA']
    for crop_name in crop_names:
        crop, created = Crop.objects.get_or_create(
            organization=org,
            name=crop_name,
            defaults={'description': f'Cultivo de {crop_name}'}
        )
        if created:
            print(f"  ✓ Creado: {crop_name}")
    crops = Crop.objects.filter(organization=org)

# Obtener parcelas sin cultivo actual
parcels_without_crop = Parcel.objects.filter(
    organization=org,
    current_crop__isnull=True
)

print(f"\nParcelas sin cultivo actual: {parcels_without_crop.count()}")

if parcels_without_crop.count() > 0:
    print("\nAsignando cultivos aleatorios a parcelas...")
    
    for parcel in parcels_without_crop[:50]:  # Limitar a 50 para no saturar
        # Asignar cultivo aleatorio
        crop = random.choice(crops)
        parcel.current_crop = crop
        parcel.save()
        print(f"  ✓ {parcel.code}: {crop.name}")

# Verificar parcelas con cultivo
parcels_with_crop = Parcel.objects.filter(
    organization=org,
    current_crop__isnull=False
)

print(f"\n" + "=" * 60)
print(f"RESULTADO:")
print(f"  - Cultivos disponibles: {crops.count()}")
print(f"  - Parcelas con cultivo: {parcels_with_crop.count()}")
print("=" * 60)

print("\nNOTA IMPORTANTE:")
print("El modelo Parcel NO tiene el campo 'planting_date'.")
print("El HarvestOptimizer necesita este campo para calcular la maduración.")
print("\nOpciones:")
print("1. Agregar el campo 'planting_date' al modelo Parcel (requiere migración)")
print("2. Modificar HarvestOptimizer para usar datos de campaigns/farm_activities")
print("3. Usar fecha de creación de la parcela como aproximación")
