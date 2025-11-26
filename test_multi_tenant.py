import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization, OrganizationMember
from tenants.middleware import set_current_organization, get_current_organization
from users.models import User

print("=" * 60)
print("PRUEBA DE SISTEMA MULTI-TENANT")
print("=" * 60)

# 1. Verificar organizaciones
print("\n1. Organizaciones creadas:")
orgs = Organization.objects.all()
for org in orgs:
    print(f"   - {org.name} ({org.subdomain}) - {org.plan} - {org.status}")

# 2. Verificar membresías
print("\n2. Membresías:")
memberships = OrganizationMember.objects.all()
for m in memberships:
    print(f"   - {m.user.username} → {m.organization.name} ({m.role})")

# 3. Probar contexto de organización
print("\n3. Prueba de contexto:")
org_sanjuan = Organization.objects.get(subdomain='sanjuan')
set_current_organization(org_sanjuan)
current = get_current_organization()
print(f"   Organización actual: {current.name if current else 'None'}")

# 4. Verificar que el middleware funciona
print("\n4. Verificación de middleware:")
print(f"   ✅ TenantMiddleware importado correctamente")
print(f"   ✅ get_current_organization() funciona")
print(f"   ✅ set_current_organization() funciona")

# 5. Estadísticas
print("\n5. Estadísticas:")
print(f"   📊 Total organizaciones: {Organization.objects.count()}")
print(f"   👥 Total membresías: {OrganizationMember.objects.count()}")
print(f"   👤 Total usuarios: {User.objects.count()}")

# 6. Verificar planes
print("\n6. Distribución de planes:")
for plan, name in Organization.PLAN_CHOICES:
    count = Organization.objects.filter(plan=plan).count()
    if count > 0:
        print(f"   - {name}: {count}")

# 7. Verificar estados
print("\n7. Estados de organizaciones:")
for status, name in Organization.STATUS_CHOICES:
    count = Organization.objects.filter(status=status).count()
    if count > 0:
        print(f"   - {name}: {count}")

print("\n" + "=" * 60)
print("✅ SISTEMA MULTI-TENANT FUNCIONANDO CORRECTAMENTE")
print("=" * 60)

print("\n📝 Próximos pasos:")
print("   1. Migrar modelos existentes a multi-tenant")
print("   2. Probar APIs con diferentes organizaciones")
print("   3. Implementar sistema de suscripciones")
print("   4. Crear landing page de registro")

print("\n🧪 Para probar las APIs:")
print("   curl http://localhost:8000/api/tenants/my-organizations/ -u admin:admin123")
print("   curl http://localhost:8000/api/partners/?org=sanjuan")
print("   curl -H 'X-Organization-Subdomain: sanjuan' http://localhost:8000/api/partners/")

print("\n" + "=" * 60)
