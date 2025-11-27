#!/usr/bin/env python
"""
Script para verificar datos del optimizador de cosecha
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from parcels.models import Parcel
from tenants.models import Organization

print("=" * 60)
print("VERIFICANDO DATOS PARA MOMENTO ÓPTIMO DE COSECHA")
print("=" * 60)

# Verificar organización sammantha
org = Organization.objects.filter(subdomain='sammantha').first()
if not org:
    print("\nERROR: Organización 'sammantha' no encontrada")
    print("\nOrganizaciones disponibles:")
    for o in Organization.objects.all():
        print(f"  - {o.name} ({o.subdomain})")
    sys.exit(1)

print(f"\nOrganización: {org.name} ({org.subdomain})")

# Verificar parcelas con cultivo
parcels_with_crop = Parcel.objects.filter(
    organization=org,
    current_crop__isnull=False
)

print(f"\nParcelas con cultivo: {parcels_with_crop.count()}")

if parcels_with_crop.count() > 0:
    print("\nPrimeras 5 parcelas:")
    for parcel in parcels_with_crop[:5]:
        print(f"  - {parcel.code}: {parcel.current_crop.name if parcel.current_crop else 'Sin cultivo'}")
else:
    print("\n⚠️ NO HAY PARCELAS CON CULTIVO ASIGNADO")
    print("\nEjecutar: python fix_harvest_optimizer_data.py")

# Verificar endpoint
print("\n" + "=" * 60)
print("PROBANDO ENDPOINT")
print("=" * 60)

from alerts.harvest_optimizer import HarvestOptimizer

optimizer = HarvestOptimizer(org)
results = optimizer.calculate_all_parcels()

print(f"\nResultados del optimizador: {len(results)} parcelas")

if len(results) > 0:
    print("\nPrimeras 3 recomendaciones:")
    for result in results[:3]:
        print(f"\n  Parcela: {result['parcel_code']}")
        print(f"  Cultivo: {result.get('crop_name', 'N/A')}")
        print(f"  Recomendación: {result['recommendation']}")
        print(f"  Score: {result['scores']['overall']}")
else:
    print("\n⚠️ EL OPTIMIZADOR NO DEVOLVIÓ RESULTADOS")
    print("\nPosibles causas:")
    print("  1. No hay parcelas con cultivo asignado")
    print("  2. Error en el cálculo del optimizador")

print("\n" + "=" * 60)
