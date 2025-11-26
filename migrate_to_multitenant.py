"""
Script para migrar todos los modelos existentes a multi-tenant.

Este script:
1. Identifica todos los modelos que necesitan migración
2. Crea una organización por defecto
3. Asigna todos los datos existentes a esa organización
4. Genera un reporte de la migración

Uso:
    python migrate_to_multitenant.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps
from django.db import connection
from tenants.models import Organization, OrganizationMember
from users.models import User


def get_models_to_migrate():
    """Identifica todos los modelos que necesitan migración a multi-tenant."""
    models_to_migrate = []
    
    # Apps que contienen modelos de negocio (excluir tenants, auth, admin, etc.)
    business_apps = [
        'partners', 'parcels', 'campaigns', 'farm_activities', 
        'inventory', 'production', 'sales', 'requests', 
        'pricing', 'shipping', 'financial', 'reports', 
        'traceability', 'analytics', 'ai_recommendations',
        'monitoring', 'weather', 'audit'
    ]
    
    for app_label in business_apps:
        try:
            app_config = apps.get_app_config(app_label)
            for model in app_config.get_models():
                # Verificar si el modelo ya tiene el campo organization
                if not hasattr(model, 'organization'):
                    models_to_migrate.append({
                        'app': app_label,
                        'model': model.__name__,
                        'model_class': model,
                        'table': model._meta.db_table
                    })
        except LookupError:
            print(f"⚠️  App '{app_label}' no encontrada")
    
    return models_to_migrate


def create_default_organization():
    """Crea o obtiene la organización por defecto."""
    org, created = Organization.objects.get_or_create(
        subdomain='default',
        defaults={
            'name': 'Cooperativa Principal',
            'slug': 'cooperativa-principal',
            'email': 'admin@cooperativa.com',
            'plan': 'ENTERPRISE',
            'status': 'ACTIVE',
            'max_users': 999,
            'max_products': 9999,
            'max_storage_mb': 10000,
            'is_active': True,
        }
    )
    
    if created:
        print(f"✅ Organización creada: {org.name}")
    else:
        print(f"ℹ️  Organización existente: {org.name}")
    
    return org


def assign_admin_to_organization(org):
    """Asigna el usuario admin a la organización como OWNER."""
    try:
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            member, created = OrganizationMember.objects.get_or_create(
                organization=org,
                user=admin_user,
                defaults={
                    'role': 'OWNER',
                    'is_active': True
                }
            )
            if created:
                print(f"✅ Usuario admin asignado como OWNER de {org.name}")
            else:
                print(f"ℹ️  Usuario admin ya es miembro de {org.name}")
    except Exception as e:
        print(f"⚠️  No se pudo asignar admin: {e}")


def check_if_column_exists(table_name, column_name):
    """Verifica si una columna existe en una tabla."""
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='{table_name}' AND column_name='{column_name}'
        """)
        return cursor.fetchone() is not None


def migrate_model_data(model_info, organization):
    """Migra los datos de un modelo a la organización por defecto."""
    model_class = model_info['model_class']
    table_name = model_info['table']
    
    # Verificar si la columna organization_id existe
    if not check_if_column_exists(table_name, 'organization_id'):
        print(f"⚠️  {model_info['model']}: Columna 'organization_id' no existe. Ejecuta makemigrations primero.")
        return 0
    
    try:
        # Contar registros sin organización
        count = model_class.objects.filter(organization__isnull=True).count()
        
        if count > 0:
            # Asignar organización
            updated = model_class.objects.filter(organization__isnull=True).update(
                organization=organization
            )
            print(f"✅ {model_info['model']}: {updated} registros migrados")
            return updated
        else:
            print(f"ℹ️  {model_info['model']}: Ya tiene organización asignada")
            return 0
    except Exception as e:
        print(f"❌ {model_info['model']}: Error - {str(e)}")
        return 0


def main():
    print("=" * 70)
    print("🚀 MIGRACIÓN A MULTI-TENANT")
    print("=" * 70)
    print()
    
    # Paso 1: Identificar modelos
    print("📋 Paso 1: Identificando modelos a migrar...")
    print("-" * 70)
    models = get_models_to_migrate()
    
    if not models:
        print("✅ Todos los modelos ya están migrados a multi-tenant!")
        return
    
    print(f"Encontrados {len(models)} modelos que necesitan migración:")
    for m in models:
        print(f"  - {m['app']}.{m['model']} (tabla: {m['table']})")
    print()
    
    # Paso 2: Crear organización por defecto
    print("📋 Paso 2: Creando organización por defecto...")
    print("-" * 70)
    org = create_default_organization()
    assign_admin_to_organization(org)
    print()
    
    # Paso 3: Migrar datos
    print("📋 Paso 3: Migrando datos existentes...")
    print("-" * 70)
    print("⚠️  IMPORTANTE: Asegúrate de haber ejecutado 'makemigrations' y 'migrate' primero!")
    print()
    
    response = input("¿Continuar con la migración de datos? (s/n): ")
    if response.lower() != 's':
        print("❌ Migración cancelada")
        return
    
    print()
    total_migrated = 0
    for model_info in models:
        migrated = migrate_model_data(model_info, org)
        total_migrated += migrated
    
    print()
    print("=" * 70)
    print("🎉 MIGRACIÓN COMPLETADA")
    print("=" * 70)
    print(f"Total de registros migrados: {total_migrated}")
    print(f"Organización: {org.name} (subdomain: {org.subdomain})")
    print()
    print("📝 Próximos pasos:")
    print("1. Verifica que todos los modelos tengan datos correctos")
    print("2. Prueba las APIs con ?org=default")
    print("3. Crea nuevas organizaciones de prueba")
    print("4. Verifica el aislamiento de datos")
    print()


if __name__ == '__main__':
    main()
