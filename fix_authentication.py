#!/usr/bin/env python
"""
Script para solucionar el problema de autenticación 403
Instala JWT y actualiza la configuración
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("SOLUCIONANDO PROBLEMA DE AUTENTICACIÓN 403")
print("=" * 60)

# Verificar usuarios y sus organizaciones
from django.contrib.auth import get_user_model
from tenants.models import Organization
from partners.models import Partner

User = get_user_model()

print("\n1. Verificando usuarios...")
users = User.objects.all()
for user in users:
    print(f"\n   Usuario: {user.username}")
    print(f"   - Email: {user.email}")
    print(f"   - Staff: {user.is_staff}")
    print(f"   - Superuser: {user.is_superuser}")
    print(f"   - Role: {user.role.name if user.role else 'Sin rol'}")
    
    # Verificar si tiene partner
    try:
        partner = Partner.objects.get(user=user)
        print(f"   - Partner: {partner.first_name} {partner.last_name}")
        print(f"   - Organizacion: {partner.organization.name if partner.organization else 'Sin organizacion'}")
    except Partner.DoesNotExist:
        print(f"   - Partner: NO TIENE PARTNER ASOCIADO [!]")

print("\n2. Verificando organizaciones...")
orgs = Organization.objects.all()
for org in orgs:
    print(f"\n   Organización: {org.name}")
    print(f"   - Subdomain: {org.subdomain}")
    print(f"   - Activa: {org.is_active}")
    partners_count = Partner.objects.filter(organization=org).count()
    print(f"   - Partners: {partners_count}")

print("\n3. Vinculando usuarios sin partner...")
# Vincular admin y superadmin si no tienen partner
admin_user = User.objects.filter(username='admin').first()
superadmin_user = User.objects.filter(username='superadmin').first()
kihomy_user = User.objects.filter(username='kihomy').first()

default_org = Organization.objects.first()

# Obtener o crear una comunidad por defecto
from partners.models import Community
default_community = Community.objects.filter(organization=default_org).first()
if not default_community:
    default_community = Community.objects.create(
        organization=default_org,
        name="Comunidad Sistema",
        description="Comunidad para usuarios administrativos"
    )
    print(f"   [OK] Comunidad por defecto creada: {default_community.name}")

if admin_user and default_org:
    try:
        partner = Partner.objects.get(user=admin_user)
        if not partner.organization:
            partner.organization = default_org
            partner.save()
            print(f"   [OK] Partner de admin vinculado a {default_org.name}")
    except Partner.DoesNotExist:
        # Crear partner para admin
        partner = Partner.objects.create(
            user=admin_user,
            organization=default_org,
            community=default_community,
            ci=f"ADM{admin_user.id}",
            first_name=admin_user.username,
            last_name="Admin",
            phone="00000000",
            address="Sistema"
        )
        print(f"   [OK] Partner creado para admin en {default_org.name}")

if superadmin_user and default_org:
    try:
        partner = Partner.objects.get(user=superadmin_user)
        if not partner.organization:
            partner.organization = default_org
            partner.save()
            print(f"   [OK] Partner de superadmin vinculado a {default_org.name}")
    except Partner.DoesNotExist:
        # Crear partner para superadmin
        partner = Partner.objects.create(
            user=superadmin_user,
            organization=default_org,
            community=default_community,
            ci=f"SUP{superadmin_user.id}",
            first_name=superadmin_user.username,
            last_name="SuperAdmin",
            phone="00000000",
            address="Sistema"
        )
        print(f"   [OK] Partner creado para superadmin en {default_org.name}")

if kihomy_user and default_org:
    try:
        partner = Partner.objects.get(user=kihomy_user)
        if not partner.organization:
            partner.organization = default_org
            partner.save()
            print(f"   [OK] Partner de kihomy vinculado a {default_org.name}")
    except Partner.DoesNotExist:
        # Crear partner para kihomy
        partner = Partner.objects.create(
            user=kihomy_user,
            organization=default_org,
            community=default_community,
            ci=f"KIH{kihomy_user.id}",
            first_name=kihomy_user.username,
            last_name="Admin",
            phone="00000000",
            address="Sistema"
        )
        print(f"   [OK] Partner creado para kihomy en {default_org.name}")

print("\n" + "=" * 60)
print("SOLUCIÓN COMPLETADA")
print("=" * 60)
print("\nPróximos pasos:")
print("1. Instalar JWT: pip install djangorestframework-simplejwt")
print("2. Actualizar settings.py con la configuración JWT")
print("3. Actualizar urls.py para incluir endpoints de token")
print("4. Reiniciar el servidor")
print("\nO simplemente ejecuta: python fix_authentication_complete.py")
