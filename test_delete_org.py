"""
Script simple para probar el endpoint de delete
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from users.models import User
from django.test import RequestFactory
from tenants.views import super_admin_delete_organization

# Crear un request factory
factory = RequestFactory()

# Obtener el superuser
try:
    superuser = User.objects.get(username='superadmin')
    print(f"✅ Superuser encontrado: {superuser.username}")
    print(f"   is_superuser: {superuser.is_superuser}")
except User.DoesNotExist:
    print("❌ Superuser no encontrado")
    exit(1)

# Obtener una organización de prueba
orgs = Organization.objects.all()
if not orgs:
    print("❌ No hay organizaciones en la base de datos")
    exit(1)

org = orgs.first()
print(f"\n📋 Organización de prueba:")
print(f"   ID: {org.id}")
print(f"   Nombre: {org.name}")
print(f"   Estado actual: {org.status}")
print(f"   is_active: {org.is_active}")

# Crear un request DELETE simulado
request = factory.delete(f'/api/tenants/super-admin/organizations/{org.id}/delete/')
request.user = superuser

print(f"\n🔄 Ejecutando delete...")
try:
    response = super_admin_delete_organization(request, org.id)
    print(f"✅ Status code: {response.status_code}")
    print(f"✅ Response: {response.data}")
    
    # Verificar cambios
    org.refresh_from_db()
    print(f"\n📋 Estado después del delete:")
    print(f"   Estado: {org.status}")
    print(f"   is_active: {org.is_active}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
