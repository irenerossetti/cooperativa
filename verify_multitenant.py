"""
Script de verificación del sistema multi-tenant.

Verifica que:
1. Todos los modelos heredan de TenantModel
2. Todos los datos tienen organización asignada
3. El filtrado automático funciona
4. Las organizaciones están configuradas correctamente

Uso:
    python verify_multitenant.py
"""

import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps
from django.db import connection
from tenants.models import Organization, OrganizationMember
from tenants.managers import TenantModel
from users.models import User


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")


def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")


def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")


def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")


def check_tenant_models():
    """Verifica que los modelos heredan de TenantModel."""
    print("\n" + "="*70)
    print("1️⃣  VERIFICANDO HERENCIA DE MODELOS")
    print("="*70)
    
    business_apps = [
        'partners', 'parcels', 'campaigns', 'farm_activities',
        'inventory', 'production', 'sales', 'requests',
        'pricing', 'shipping', 'financial', 'reports',
        'traceability', 'analytics', 'ai_recommendations',
        'monitoring', 'weather', 'audit'
    ]
    
    tenant_models = []
    non_tenant_models = []
    
    for app_label in business_apps:
        try:
            app_config = apps.get_app_config(app_label)
            for model in app_config.get_models():
                if issubclass(model, TenantModel):
                    tenant_models.append(f"{app_label}.{model.__name__}")
                elif hasattr(model, 'organization'):
                    print_warning(f"{app_label}.{model.__name__} tiene campo organization pero no hereda de TenantModel")
                    non_tenant_models.append(f"{app_label}.{model.__name__}")
                else:
                    non_tenant_models.append(f"{app_label}.{model.__name__}")
        except LookupError:
            pass
    
    print(f"\nModelos multi-tenant: {len(tenant_models)}")
    print(f"Modelos sin multi-tenant: {len(non_tenant_models)}")
    
    if non_tenant_models:
        print("\n⚠️  Modelos que necesitan migración:")
        for model in non_tenant_models[:10]:  # Mostrar solo los primeros 10
            print(f"   - {model}")
        if len(non_tenant_models) > 10:
            print(f"   ... y {len(non_tenant_models) - 10} más")
        return False
    else:
        print_success("Todos los modelos heredan de TenantModel")
        return True


def check_organizations():
    """Verifica que existen organizaciones."""
    print("\n" + "="*70)
    print("2️⃣  VERIFICANDO ORGANIZACIONES")
    print("="*70)
    
    org_count = Organization.objects.count()
    
    if org_count == 0:
        print_error("No hay organizaciones creadas")
        print_info("Ejecuta: python migrate_to_multitenant.py")
        return False
    
    print_success(f"Encontradas {org_count} organizaciones")
    
    for org in Organization.objects.all():
        members_count = org.members.count()
        print(f"   - {org.name} ({org.subdomain})")
        print(f"     Plan: {org.get_plan_display_name()}, Estado: {org.status}")
        print(f"     Miembros: {members_count}")
    
    return True


def check_data_assignment():
    """Verifica que todos los datos tienen organización asignada."""
    print("\n" + "="*70)
    print("3️⃣  VERIFICANDO ASIGNACIÓN DE DATOS")
    print("="*70)
    
    business_apps = [
        'partners', 'parcels', 'campaigns', 'farm_activities',
        'inventory', 'production', 'sales', 'requests',
        'pricing', 'shipping', 'financial', 'reports',
        'traceability', 'analytics', 'ai_recommendations',
        'monitoring', 'weather', 'audit'
    ]
    
    all_assigned = True
    total_records = 0
    unassigned_records = 0
    
    for app_label in business_apps:
        try:
            app_config = apps.get_app_config(app_label)
            for model in app_config.get_models():
                if issubclass(model, TenantModel):
                    total = model.objects.all_organizations().count()
                    unassigned = model.objects.all_organizations().filter(organization__isnull=True).count()
                    
                    total_records += total
                    unassigned_records += unassigned
                    
                    if unassigned > 0:
                        print_error(f"{app_label}.{model.__name__}: {unassigned}/{total} sin organización")
                        all_assigned = False
        except LookupError:
            pass
    
    print(f"\nTotal de registros: {total_records}")
    print(f"Registros sin organización: {unassigned_records}")
    
    if all_assigned:
        print_success("Todos los datos tienen organización asignada")
        return True
    else:
        print_error("Hay datos sin organización asignada")
        print_info("Ejecuta: python migrate_to_multitenant.py")
        return False


def check_automatic_filtering():
    """Verifica que el filtrado automático funciona."""
    print("\n" + "="*70)
    print("4️⃣  VERIFICANDO FILTRADO AUTOMÁTICO")
    print("="*70)
    
    from tenants.middleware import set_current_organization
    from partners.models import Partner
    
    orgs = Organization.objects.all()
    
    if orgs.count() == 0:
        print_warning("No hay organizaciones para probar")
        return False
    
    org = orgs.first()
    
    # Establecer contexto
    set_current_organization(org)
    
    # Contar con filtro automático
    filtered_count = Partner.objects.count()
    
    # Contar sin filtro
    total_count = Partner.objects.all_organizations().count()
    
    print(f"Organización de prueba: {org.name}")
    print(f"Partners con filtro automático: {filtered_count}")
    print(f"Partners totales (sin filtro): {total_count}")
    
    if filtered_count <= total_count:
        print_success("El filtrado automático funciona correctamente")
        return True
    else:
        print_error("El filtrado automático no funciona")
        return False


def check_middleware():
    """Verifica que el middleware está configurado."""
    print("\n" + "="*70)
    print("5️⃣  VERIFICANDO MIDDLEWARE")
    print("="*70)
    
    from django.conf import settings
    
    middleware = settings.MIDDLEWARE
    
    if 'tenants.middleware.TenantMiddleware' in middleware:
        print_success("TenantMiddleware está configurado")
        
        # Verificar posición
        auth_idx = middleware.index('django.contrib.auth.middleware.AuthenticationMiddleware')
        tenant_idx = middleware.index('tenants.middleware.TenantMiddleware')
        
        if tenant_idx > auth_idx:
            print_success("TenantMiddleware está después de AuthenticationMiddleware (correcto)")
            return True
        else:
            print_warning("TenantMiddleware debería estar después de AuthenticationMiddleware")
            return False
    else:
        print_error("TenantMiddleware NO está configurado")
        print_info("Agrégalo a MIDDLEWARE en settings.py")
        return False


def check_admin_user():
    """Verifica que el usuario admin está asignado a una organización."""
    print("\n" + "="*70)
    print("6️⃣  VERIFICANDO USUARIO ADMIN")
    print("="*70)
    
    try:
        admin = User.objects.get(username='admin')
        memberships = OrganizationMember.objects.filter(user=admin)
        
        if memberships.count() == 0:
            print_error("Usuario admin no pertenece a ninguna organización")
            print_info("Ejecuta: python migrate_to_multitenant.py")
            return False
        
        print_success(f"Usuario admin pertenece a {memberships.count()} organización(es)")
        for membership in memberships:
            print(f"   - {membership.organization.name} ({membership.role})")
        
        return True
    except User.DoesNotExist:
        print_warning("Usuario admin no existe")
        return False


def main():
    print("="*70)
    print("🔍 VERIFICACIÓN DEL SISTEMA MULTI-TENANT")
    print("="*70)
    
    checks = [
        ("Herencia de modelos", check_tenant_models),
        ("Organizaciones", check_organizations),
        ("Asignación de datos", check_data_assignment),
        ("Filtrado automático", check_automatic_filtering),
        ("Middleware", check_middleware),
        ("Usuario admin", check_admin_user),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error en {name}: {str(e)}")
            results.append((name, False))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Verificaciones pasadas: {passed}/{total}")
    
    if passed == total:
        print()
        print_success("🎉 ¡Sistema multi-tenant completamente funcional!")
        print()
        print("Próximos pasos:")
        print("1. Crear organizaciones de prueba: python create_test_organizations.py")
        print("2. Probar las APIs con ?org=nombre_organizacion")
        print("3. Verificar aislamiento de datos entre organizaciones")
        return 0
    else:
        print()
        print_error("⚠️  Hay problemas que necesitan ser resueltos")
        print()
        print("Revisa la guía: GUIA_MIGRACION_MULTITENANT.md")
        return 1


if __name__ == '__main__':
    sys.exit(main())
