#!/usr/bin/env python
"""Script para vincular el usuario mooncaker a un partner en San Juan"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from partners.models import Partner
from tenants.models import Organization

print("=" * 80)
print("VINCULAR USUARIO A PARTNER")
print("=" * 80)

# Obtener usuario
user = User.objects.get(email='mooncaker@gmail.com')
print(f"\n✅ Usuario: {user.username} ({user.email})")

# Obtener organización San Juan
org_sanjuan = Organization.objects.get(subdomain='sanjuan')
print(f"✅ Organización: {org_sanjuan.name}")

# Buscar un partner sin usuario en San Juan
partner = Partner.objects.all_organizations().filter(
    organization=org_sanjuan,
    ci='11111111'
).first()

if partner:
    print(f"\n📋 Partner encontrado:")
    print(f"   Nombre: {partner.full_name}")
    print(f"   CI: {partner.ci}")
    print(f"   Usuario actual: {partner.user if partner.user else 'Sin usuario'}")
    
    # Vincular
    partner.user = user
    partner.save()
    
    print(f"\n✅ VINCULACIÓN EXITOSA")
    print(f"   {partner.full_name} ahora está vinculado al usuario {user.username}")
    print(f"   Ahora {user.username} puede loguearse en {org_sanjuan.name}")
else:
    print(f"\n❌ No se encontró el partner con CI 11111111 en San Juan")

print("\n" + "=" * 80)
