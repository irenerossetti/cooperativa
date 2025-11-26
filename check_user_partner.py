#!/usr/bin/env python
"""Script para verificar si un usuario tiene partner asociado"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from partners.models import Partner

print("=" * 80)
print("VERIFICAR USUARIO Y SU PARTNER")
print("=" * 80)

# Buscar usuario por email
email = "mooncaker@gmail.com"
try:
    user = User.objects.get(email=email)
    print(f"\n✅ Usuario encontrado:")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Rol: {user.role.name if user.role else 'Sin rol'}")
    print(f"   Superuser: {user.is_superuser}")
    
    # Buscar partner asociado
    try:
        partner = Partner.objects.all_organizations().get(user=user)
        print(f"\n✅ Partner asociado:")
        print(f"   Nombre: {partner.full_name}")
        print(f"   CI: {partner.ci}")
        print(f"   Organización: {partner.organization.name}")
        print(f"   Subdomain: {partner.organization.subdomain}")
    except Partner.DoesNotExist:
        print(f"\n❌ NO tiene partner asociado")
        print(f"   El usuario existe pero no está vinculado a ningún partner")
        
        # Buscar partners sin usuario
        print(f"\n📋 Partners sin usuario asignado:")
        partners_sin_user = Partner.objects.all_organizations().filter(user__isnull=True)[:5]
        for p in partners_sin_user:
            print(f"   - {p.full_name} (CI: {p.ci}) en {p.organization.name}")
            
except User.DoesNotExist:
    print(f"\n❌ Usuario con email '{email}' NO encontrado")

print("\n" + "=" * 80)
