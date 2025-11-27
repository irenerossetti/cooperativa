"""
Configurar usuarios de demo: admin, socios y clientes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from tenants.models import Organization, OrganizationMember
from partners.models import Partner

User = get_user_model()

def setup_users():
    print("🔧 Configurando usuarios de demo...")
    
    org = Organization.objects.filter(name="Cooperativa San Juan").first()
    if not org:
        print("❌ No existe 'Cooperativa San Juan'")
        return
    
    print(f"✓ Organización: {org.name}\n")
    
    # 1. Vincular usuarios admin existentes
    print("👤 ADMINISTRADORES:")
    for username in ['superadmin', 'admin']:
        user = User.objects.filter(username=username).first()
        if user:
            OrganizationMember.objects.get_or_create(
                user=user, organization=org,
                defaults={'role': 'admin'}
            )
            print(f"  ✓ {username} / admin123 (ADMIN)")
    
    # 2. Crear usuarios socio
    print("\n👥 SOCIOS:")
    socios_data = [
        ('socio1', 'Juan', 'Pérez', '2000001'),
        ('socio2', 'María', 'González', '2000002'),
    ]
    
    for username, first, last, ci in socios_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@coop.com', 'first_name': first, 'last_name': last}
        )
        if created:
            user.set_password('socio123')
            user.save()
        
        OrganizationMember.objects.get_or_create(
            user=user, organization=org,
            defaults={'role': 'member'}
        )
        
        partner, _ = Partner.objects.get_or_create(
            ci=ci, organization=org,
            defaults={
                'first_name': first, 'last_name': last,
                'email': f'{username}@coop.com',
                'phone': '+5492644100000',
                'status': 'ACTIVE',
                'user': user
            }
        )
        print(f"  ✓ {username} / socio123 (SOCIO)")
    
    # 3. Crear usuarios cliente
    print("\n🛒 CLIENTES:")
    clientes_data = [
        ('cliente1', 'Pedro', 'Martínez'),
        ('cliente2', 'Ana', 'López'),
    ]
    
    for username, first, last in clientes_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@mail.com', 'first_name': first, 'last_name': last}
        )
        if created:
            user.set_password('cliente123')
            user.save()
        
        OrganizationMember.objects.get_or_create(
            user=user, organization=org,
            defaults={'role': 'member'}
        )
        print(f"  ✓ {username} / cliente123 (CLIENTE)")
    
    print("\n" + "="*50)
    print("✅ USUARIOS CONFIGURADOS")
    print("="*50)

if __name__ == '__main__':
    setup_users()
