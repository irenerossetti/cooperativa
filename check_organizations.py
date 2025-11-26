#!/usr/bin/env python
"""Script para verificar las organizaciones y sus subdominios"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from partners.models import Partner

print("=" * 60)
print("ORGANIZACIONES EN LA BASE DE DATOS")
print("=" * 60)

orgs = Organization.objects.all()
for org in orgs:
    print(f"\n📍 {org.name}")
    print(f"   Subdomain: {org.subdomain}")
    print(f"   Activa: {org.is_active}")
    
    # Contar partners
    partner_count = Partner.objects.filter(organization=org).count()
    print(f"   Partners: {partner_count}")
    
    if partner_count > 0:
        print(f"   Primeros 3 partners:")
        partners = Partner.objects.filter(organization=org)[:3]
        for p in partners:
            print(f"      - {p.full_name} (CI: {p.ci})")

print("\n" + "=" * 60)
print(f"Total organizaciones: {orgs.count()}")
print("=" * 60)
