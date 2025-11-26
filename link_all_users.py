#!/usr/bin/env python
"""Script para vincular todos los usuarios sin partner a partners disponibles"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from partners.models import Partner
from tenants.models import Organization

print("=" * 80)
print("VINCULAR USUARIOS A PARTNERS")
print("=" * 80)

# Obtener organización San Juan
org_sanjuan = Organization.objects.get(subdomain='sanjuan')

# Usuarios sin partner
users_sin_partner = User.objects.filter(partner__isnull=True, is_superuser=False)
print(f"\n📋 Usuarios sin partner: {users_sin_partner.count()}")

# Partners sin usuario en San Juan
partners_sin_user = Partner.objects.all_organizations().filter(
    organization=org_sanjuan,
    user__isnull=True
)
print(f"📋 Partners sin usuario en San Juan: {partners_sin_user.count()}")

# Vincular
vinculados = 0
for user in users_sin_partner:
    if partners_sin_user.exists():
        partner = partners_sin_user.first()
        partner.user = user
        partner.save()
        
        print(f"\n✅ Vinculado:")
        print(f"   Usuario: {user.username} ({user.email})")
        print(f"   Partner: {partner.full_name} (CI: {partner.ci})")
        print(f"   Organización: {partner.organization.name}")
        
        vinculados += 1
        # Actualizar queryset
        partners_sin_user = Partner.objects.all_organizations().filter(
            organization=org_sanjuan,
            user__isnull=True
        )
    else:
        print(f"\n⚠️  No hay más partners disponibles para: {user.username}")
        break

print(f"\n" + "=" * 80)
print(f"✅ Total vinculados: {vinculados}")
print("=" * 80)
