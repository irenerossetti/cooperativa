#!/usr/bin/env python
"""Script para configurar permisos por defecto en los roles"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import Role

# Permisos por defecto para cada rol
DEFAULT_PERMISSIONS = {
    'ADMIN': {
        'users': {'view': True, 'create': True, 'edit': True, 'delete': True},
        'partners': {'view': True, 'create': True, 'edit': True, 'delete': True},
        'products': {'view': True, 'create': True, 'edit': True, 'delete': True},
        'sales': {'view': True, 'create': True, 'edit': True, 'delete': True},
        'campaigns': {'view': True, 'create': True, 'edit': True, 'delete': True},
        'reports': {'view': True, 'export': True},
        'settings': {'view': True, 'edit': True},
        'ui': {
            'show_delete_buttons': True,
            'show_prices': True,
            'show_costs': True,
            'show_reports': True,
        }
    },
    'PARTNER': {
        'users': {'view': False, 'create': False, 'edit': False, 'delete': False},
        'partners': {'view': True, 'create': False, 'edit': False, 'delete': False},
        'products': {'view': True, 'create': False, 'edit': False, 'delete': False},
        'sales': {'view': True, 'create': True, 'edit': False, 'delete': False},
        'campaigns': {'view': True, 'create': False, 'edit': False, 'delete': False},
        'reports': {'view': True, 'export': False},
        'settings': {'view': False, 'edit': False},
        'ui': {
            'show_delete_buttons': False,
            'show_prices': True,
            'show_costs': False,
            'show_reports': True,
        }
    },
    'OPERATOR': {
        'users': {'view': True, 'create': True, 'edit': True, 'delete': False},
        'partners': {'view': True, 'create': True, 'edit': True, 'delete': False},
        'products': {'view': True, 'create': True, 'edit': True, 'delete': False},
        'sales': {'view': True, 'create': True, 'edit': True, 'delete': False},
        'campaigns': {'view': True, 'create': True, 'edit': True, 'delete': False},
        'reports': {'view': True, 'export': True},
        'settings': {'view': True, 'edit': False},
        'ui': {
            'show_delete_buttons': False,
            'show_prices': True,
            'show_costs': True,
            'show_reports': True,
        }
    }
}

print("=" * 80)
print("CONFIGURANDO PERMISOS POR DEFECTO")
print("=" * 80)

for role_name, permissions in DEFAULT_PERMISSIONS.items():
    role, created = Role.objects.get_or_create(
        name=role_name,
        defaults={
            'description': f'Rol {role_name} con permisos predefinidos',
            'permissions': permissions,
            'is_active': True
        }
    )
    
    if not created:
        # Actualizar permisos si el rol ya existe
        role.permissions = permissions
        role.save()
        print(f"\n✅ Actualizado: {role_name}")
    else:
        print(f"\n✅ Creado: {role_name}")
    
    print(f"   Permisos configurados:")
    for module, perms in permissions.items():
        if isinstance(perms, dict):
            enabled = [k for k, v in perms.items() if v]
            print(f"      - {module}: {', '.join(enabled)}")

print("\n" + "=" * 80)
print("✅ Permisos configurados exitosamente")
print("=" * 80)
