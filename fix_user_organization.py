"""
Script para vincular usuarios existentes a la organización
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from tenants.models import Organization, OrganizationMember
from partners.models import Partner

User = get_user_model()

def fix_users():
    print("🔧 Vinculando usuarios a organización...")
    
    # Obtener organización
    org = Organization.objects.first()
    if not org:
        print("❌ No hay organizaciones")
        return
    
    print(f"✓ Organización: {org.name}")
    
    # Vincular todos los usuarios a la organización
    users = User.objects.all()
    for user in users:
        # Crear membership si no existe
        member, created = OrganizationMember.objects.get_or_create(
            user=user,
            organization=org,
            defaults={'role': 'admin' if user.is_staff else 'member'}
        )
        
        if created:
            print(f"✓ Usuario {user.username} vinculado como {member.role}")
        
        # Si el usuario no tiene partner, intentar vincularlo
        if not hasattr(user, 'partner'):
            # Buscar un partner sin usuario
            partner = Partner.objects.filter(user__isnull=True, organization=org).first()
            if partner:
                partner.user = user
                partner.save()
                print(f"✓ Usuario {user.username} vinculado a socio {partner.ci}")
    
    print("\n✅ Usuarios vinculados correctamente")
    print(f"Total usuarios: {users.count()}")
    print(f"Total miembros: {OrganizationMember.objects.filter(organization=org).count()}")

if __name__ == '__main__':
    fix_users()
