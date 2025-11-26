#!/usr/bin/env python
"""Script de SOLO LECTURA para verificar a qué organización pertenece cada partner"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from partners.models import Partner

print("=" * 80)
print("DIAGNÓSTICO: PARTNERS Y SUS ORGANIZACIONES")
print("=" * 80)

# Obtener todos los partners SIN filtro de tenant
all_partners = Partner.objects.all_organizations()

print(f"\n📊 Total de partners en la BD (sin filtro): {all_partners.count()}")

# Agrupar por organización
org_dict = {}
for partner in all_partners:
    org_name = partner.organization.name if partner.organization else "SIN ORGANIZACIÓN"
    if org_name not in org_dict:
        org_dict[org_name] = []
    org_dict[org_name].append(partner)

print("\n" + "=" * 80)
print("DISTRIBUCIÓN POR ORGANIZACIÓN:")
print("=" * 80)

for org_name, partners in org_dict.items():
    print(f"\n📍 {org_name}: {len(partners)} partners")
    for p in partners:
        print(f"   - {p.full_name} (CI: {p.ci}) [org_id: {p.organization_id}]")

print("\n" + "=" * 80)
print("VERIFICACIÓN DEL FILTRO DE TENANT:")
print("=" * 80)

# Probar el filtro con cada organización
from tenants.middleware import set_current_organization

orgs = Organization.objects.all()[:3]  # Primeras 3 organizaciones

for org in orgs:
    set_current_organization(org)
    filtered_count = Partner.objects.count()
    print(f"\n🔍 Organización: {org.name} (subdomain: {org.subdomain})")
    print(f"   Partners filtrados: {filtered_count}")
    
    if filtered_count > 0:
        partners = Partner.objects.all()[:3]
        for p in partners:
            print(f"      - {p.full_name}")

# Limpiar
set_current_organization(None)

print("\n" + "=" * 80)
print("CONCLUSIÓN:")
print("=" * 80)
print("Si todos los partners tienen el mismo organization_id,")
print("entonces el problema es que los datos NO están distribuidos.")
print("El filtro funciona, pero todos apuntan a la misma organización.")
print("=" * 80)
