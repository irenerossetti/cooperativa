import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User, Role
from partners.models import Partner

print("=" * 60)
print("CREANDO USUARIOS DE PRUEBA CON ROLES")
print("=" * 60)

# 1. CREAR ROLES SI NO EXISTEN
print("\n📋 Creando roles...")

roles_data = [
    {'name': 'ADMIN', 'description': 'Administrador del sistema'},
    {'name': 'PARTNER', 'description': 'Socio de la cooperativa'},
    {'name': 'CUSTOMER', 'description': 'Cliente'},
]

roles = {}
for role_data in roles_data:
    role, created = Role.objects.get_or_create(
        name=role_data['name'],
        defaults={'description': role_data['description']}
    )
    roles[role_data['name']] = role
    status = "✅ Creado" if created else "ℹ️  Ya existe"
    print(f"{status}: {role.name} - {role.description}")

# 2. CREAR USUARIO ADMINISTRADOR
print("\n👤 Creando usuario ADMINISTRADOR...")
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@cooperativa.com',
        'first_name': 'Admin',
        'last_name': 'Sistema',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    }
)
admin_user.set_password('admin123')
admin_user.role = roles['ADMIN']
admin_user.save()
print(f"✅ Usuario: admin / admin123")
print(f"   Email: {admin_user.email}")
print(f"   Rol: ADMIN")

# 3. CREAR USUARIO SOCIO
print("\n👤 Creando usuario SOCIO...")
socio_user, created = User.objects.get_or_create(
    username='socio',
    defaults={
        'email': 'socio@cooperativa.com',
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'is_staff': False,
        'is_superuser': False,
        'is_active': True,
    }
)
socio_user.set_password('socio123')
socio_user.role = roles['PARTNER']
socio_user.save()
print(f"✅ Usuario: socio / socio123")
print(f"   Email: {socio_user.email}")
print(f"   Rol: PARTNER")

# Crear comunidad si no existe
from partners.models import Community
community, created = Community.objects.get_or_create(
    name='Comunidad Central',
    defaults={
        'description': 'Comunidad principal de la cooperativa',
        'is_active': True,
    }
)

# Crear registro de socio si no existe
partner, created = Partner.objects.get_or_create(
    ci='12345678',
    defaults={
        'user': socio_user,
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'phone': '+59112345678',
        'address': 'Calle Principal #123',
        'community': community,
        'status': 'ACTIVE',
    }
)
if created:
    print(f"   ✅ Registro de socio creado")
else:
    partner.user = socio_user
    partner.save()
    print(f"   ℹ️  Registro de socio actualizado")

# 4. CREAR USUARIO CLIENTE
print("\n👤 Creando usuario CLIENTE...")
cliente_user, created = User.objects.get_or_create(
    username='cliente',
    defaults={
        'email': 'cliente@email.com',
        'first_name': 'María',
        'last_name': 'González',
        'is_staff': False,
        'is_superuser': False,
        'is_active': True,
    }
)
cliente_user.set_password('cliente123')
cliente_user.role = roles['CUSTOMER']
cliente_user.save()
print(f"✅ Usuario: cliente / cliente123")
print(f"   Email: {cliente_user.email}")
print(f"   Rol: CUSTOMER")

# 5. CREAR MÁS USUARIOS DE PRUEBA
print("\n👥 Creando usuarios adicionales...")

# Socio 2
socio2_user, created = User.objects.get_or_create(
    username='socio2',
    defaults={
        'email': 'socio2@cooperativa.com',
        'first_name': 'Pedro',
        'last_name': 'Mamani',
        'is_staff': False,
        'is_superuser': False,
        'is_active': True,
    }
)
socio2_user.set_password('socio123')
socio2_user.role = roles['PARTNER']
socio2_user.save()
print(f"✅ Usuario: socio2 / socio123 (PARTNER)")

partner2, created = Partner.objects.get_or_create(
    ci='87654321',
    defaults={
        'user': socio2_user,
        'first_name': 'Pedro',
        'last_name': 'Mamani',
        'phone': '+59187654321',
        'address': 'Av. Libertad #456',
        'community': community,
        'status': 'ACTIVE',
    }
)

# Cliente 2
cliente2_user, created = User.objects.get_or_create(
    username='cliente2',
    defaults={
        'email': 'cliente2@email.com',
        'first_name': 'Ana',
        'last_name': 'Quispe',
        'is_staff': False,
        'is_superuser': False,
        'is_active': True,
    }
)
cliente2_user.set_password('cliente123')
cliente2_user.role = roles['CUSTOMER']
cliente2_user.save()
print(f"✅ Usuario: cliente2 / cliente123 (CUSTOMER)")

print("\n" + "=" * 60)
print("RESUMEN DE USUARIOS CREADOS")
print("=" * 60)
print("\n🔐 CREDENCIALES DE ACCESO:\n")
print("ADMINISTRADOR:")
print("  Usuario: admin")
print("  Password: admin123")
print("  Rol: ADMIN\n")

print("SOCIO 1:")
print("  Usuario: socio")
print("  Password: socio123")
print("  Rol: PARTNER\n")

print("SOCIO 2:")
print("  Usuario: socio2")
print("  Password: socio123")
print("  Rol: PARTNER\n")

print("CLIENTE 1:")
print("  Usuario: cliente")
print("  Password: cliente123")
print("  Rol: CUSTOMER\n")

print("CLIENTE 2:")
print("  Usuario: cliente2")
print("  Password: cliente123")
print("  Rol: CUSTOMER\n")

print("=" * 60)
print("✅ PROCESO COMPLETADO")
print("=" * 60)
