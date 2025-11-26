import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization, OrganizationMember
from users.models import User
from datetime import timedelta
from django.utils import timezone
import random

print("=" * 70)
print("🏢 CREANDO ORGANIZACIÓN DE DEMOSTRACIÓN")
print("=" * 70)

# Generar un número aleatorio para evitar duplicados
numero = random.randint(1000, 9999)

# Datos de la organización
org_data = {
    'name': f'Cooperativa Demo {numero}',
    'subdomain': f'demo{numero}',
    'email': f'contacto@demo{numero}.com',
    'phone': '+591 3 1234567',
    'plan': 'PROFESSIONAL',
    'status': 'ACTIVE',
    'max_users': 20,
    'max_products': 1000,
    'max_storage_mb': 1000,
    'trial_ends_at': timezone.now() + timedelta(days=30),
}

print(f"\n📋 Datos de la organización:")
print(f"   Nombre: {org_data['name']}")
print(f"   Subdominio: {org_data['subdomain']}")
print(f"   Email: {org_data['email']}")
print(f"   Plan: {org_data['plan']}")

# Crear la organización
print(f"\n⏳ Creando organización...")
org = Organization.objects.create(**org_data)
print(f"✅ Organización creada con ID: {org.id}")

# Datos del usuario administrador
user_data = {
    'username': f'admin{numero}',
    'email': f'admin@demo{numero}.com',
    'first_name': 'Admin',
    'last_name': 'Demo',
}

print(f"\n👤 Datos del usuario administrador:")
print(f"   Username: {user_data['username']}")
print(f"   Email: {user_data['email']}")
print(f"   Password: demo123456")

# Crear el usuario
print(f"\n⏳ Creando usuario...")
user = User.objects.create_user(
    username=user_data['username'],
    email=user_data['email'],
    password='demo123456',
    first_name=user_data['first_name'],
    last_name=user_data['last_name']
)
print(f"✅ Usuario creado con ID: {user.id}")

# Crear la membresía
print(f"\n⏳ Asignando usuario como propietario...")
membership = OrganizationMember.objects.create(
    organization=org,
    user=user,
    role='OWNER',
    is_active=True
)
print(f"✅ Membresía creada")

print("\n" + "=" * 70)
print("🎉 ¡ORGANIZACIÓN DE DEMOSTRACIÓN CREADA EXITOSAMENTE!")
print("=" * 70)

print(f"\n📝 INFORMACIÓN PARA LA DEMOSTRACIÓN:")
print(f"\n🏢 ORGANIZACIÓN:")
print(f"   Nombre: {org.name}")
print(f"   Subdominio: {org.subdomain}")
print(f"   Plan: {org.plan}")
print(f"   Estado: {org.status}")

print(f"\n👤 CREDENCIALES DE ACCESO:")
print(f"   Usuario: {user.username}")
print(f"   Password: demo123456")
print(f"   Email: {user.email}")

print(f"\n🔗 CÓMO ACCEDER A ESTA ORGANIZACIÓN:")
print(f"\n   Opción 1 - Query Parameter:")
print(f"   http://localhost:8000/api/partners/?org={org.subdomain}")
print(f"   http://localhost:5173/?org={org.subdomain}")

print(f"\n   Opción 2 - Header HTTP:")
print(f"   X-Organization-Subdomain: {org.subdomain}")

print(f"\n   Opción 3 - Subdominio (requiere configuración DNS):")
print(f"   http://{org.subdomain}.localhost:8000")

print(f"\n💡 PARA HACER LOGIN:")
print(f"   1. Ve a: http://localhost:5173/login?org={org.subdomain}")
print(f"   2. Usuario: {user.username}")
print(f"   3. Password: demo123456")

print(f"\n📊 PRÓXIMOS PASOS:")
print(f"   1. Hacer login con las credenciales")
print(f"   2. Crear productos para esta organización")
print(f"   3. Crear socios")
print(f"   4. Hacer ventas")
print(f"   5. Todo estará aislado en esta organización")

print("\n" + "=" * 70)
print("✨ ¡LISTO PARA LA DEMOSTRACIÓN!")
print("=" * 70)
