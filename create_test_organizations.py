import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization, OrganizationMember
from users.models import User
from datetime import timedelta
from django.utils import timezone

print("=" * 60)
print("CREANDO ORGANIZACIONES DE PRUEBA")
print("=" * 60)

# Crear organizaciones de prueba
organizations_data = [
    {
        'name': 'Cooperativa San Juan',
        'subdomain': 'sanjuan',
        'email': 'contacto@sanjuan.coop',
        'phone': '+591 3 1234567',
        'plan': 'PROFESSIONAL',
        'status': 'ACTIVE',
    },
    {
        'name': 'Cooperativa El Progreso',
        'subdomain': 'progreso',
        'email': 'info@progreso.coop',
        'phone': '+591 3 7654321',
        'plan': 'BASIC',
        'status': 'ACTIVE',
    },
    {
        'name': 'Cooperativa Demo',
        'subdomain': 'demo',
        'email': 'demo@cooperativa.com',
        'phone': '+591 3 9999999',
        'plan': 'FREE',
        'status': 'TRIAL',
    },
]

created_orgs = []

for org_data in organizations_data:
    org, created = Organization.objects.get_or_create(
        subdomain=org_data['subdomain'],
        defaults={
            **org_data,
            'trial_ends_at': timezone.now() + timedelta(days=30),
            'max_users': 20 if org_data['plan'] == 'PROFESSIONAL' else 10,
            'max_products': 1000 if org_data['plan'] == 'PROFESSIONAL' else 500,
            'max_storage_mb': 1000 if org_data['plan'] == 'PROFESSIONAL' else 500,
        }
    )
    
    if created:
        print(f"✅ Creada: {org.name} ({org.subdomain})")
        created_orgs.append(org)
    else:
        print(f"ℹ️  Ya existe: {org.name} ({org.subdomain})")
        created_orgs.append(org)

print("\n" + "=" * 60)
print("ASIGNANDO USUARIOS A ORGANIZACIONES")
print("=" * 60)

# Obtener o crear usuarios de prueba
admin_user, _ = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@cooperativa.com',
        'first_name': 'Admin',
        'last_name': 'Sistema',
        'is_staff': True,
        'is_superuser': True,
    }
)
if _:
    admin_user.set_password('admin123')
    admin_user.save()
    print(f"✅ Usuario admin creado")

socio_user, _ = User.objects.get_or_create(
    username='socio1',
    defaults={
        'email': 'socio1@cooperativa.com',
        'first_name': 'Juan',
        'last_name': 'Pérez',
    }
)
if _:
    socio_user.set_password('socio123')
    socio_user.save()
    print(f"✅ Usuario socio1 creado")

cliente_user, _ = User.objects.get_or_create(
    username='cliente1',
    defaults={
        'email': 'cliente1@cooperativa.com',
        'first_name': 'María',
        'last_name': 'González',
    }
)
if _:
    cliente_user.set_password('cliente123')
    cliente_user.save()
    print(f"✅ Usuario cliente1 creado")

# Asignar usuarios a organizaciones
print("\n" + "=" * 60)
print("CREANDO MEMBRESÍAS")
print("=" * 60)

memberships = [
    # Admin es owner de todas las organizaciones
    {'org': created_orgs[0], 'user': admin_user, 'role': 'OWNER'},
    {'org': created_orgs[1], 'user': admin_user, 'role': 'OWNER'},
    {'org': created_orgs[2], 'user': admin_user, 'role': 'OWNER'},
    
    # Socio es admin de San Juan
    {'org': created_orgs[0], 'user': socio_user, 'role': 'ADMIN'},
    
    # Cliente es member de San Juan
    {'org': created_orgs[0], 'user': cliente_user, 'role': 'MEMBER'},
]

for membership_data in memberships:
    membership, created = OrganizationMember.objects.get_or_create(
        organization=membership_data['org'],
        user=membership_data['user'],
        defaults={'role': membership_data['role']}
    )
    
    if created:
        print(f"✅ {membership_data['user'].username} → {membership_data['org'].name} ({membership_data['role']})")
    else:
        print(f"ℹ️  Ya existe: {membership_data['user'].username} → {membership_data['org'].name}")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"📊 Organizaciones: {Organization.objects.count()}")
print(f"👥 Membresías: {OrganizationMember.objects.count()}")
print("\n🎉 ¡Organizaciones de prueba creadas!")
print("\n📝 Puedes acceder usando:")
print("   - Subdominio: sanjuan.localhost:5173")
print("   - Header: X-Organization-Subdomain: sanjuan")
print("   - Query: ?org=sanjuan")
print("\n👤 Usuarios de prueba:")
print("   - admin / admin123 (Owner)")
print("   - socio1 / socio123 (Admin)")
print("   - cliente1 / cliente123 (Member)")
print("=" * 60)
