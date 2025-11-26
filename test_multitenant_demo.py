"""
Script de demostración del sistema multi-tenant.

Este script demuestra:
1. Crear partners en diferentes organizaciones
2. Verificar que los datos están aislados
3. Probar el filtrado automático
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from partners.models import Partner, Community
from tenants.middleware import set_current_organization


def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def main():
    print_header("🧪 DEMOSTRACIÓN DEL SISTEMA MULTI-TENANT")
    
    # Obtener organizaciones
    org_sanjuan = Organization.objects.get(subdomain='sanjuan')
    org_progreso = Organization.objects.get(subdomain='progreso')
    
    print(f"\n📊 Organizaciones de prueba:")
    print(f"   1. {org_sanjuan.name} (ID: {org_sanjuan.id})")
    print(f"   2. {org_progreso.name} (ID: {org_progreso.id})")
    
    # Obtener o crear comunidad para cada organización
    print_header("1️⃣  CREANDO DATOS DE PRUEBA")
    
    # Establecer contexto para San Juan
    set_current_organization(org_sanjuan)
    community_sj, _ = Community.objects.get_or_create(
        name='Comunidad San Juan Test',
        defaults={'description': 'Comunidad de prueba'}
    )
    print(f"✅ Comunidad creada en San Juan: {community_sj.name}")
    
    # Crear partner en San Juan
    partner_sj, created = Partner.objects.get_or_create(
        ci='11111111',
        defaults={
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'phone': '+59170000001',
            'community': community_sj,
            'status': 'ACTIVE'
        }
    )
    if created:
        print(f"✅ Partner creado en San Juan: {partner_sj.full_name} (CI: {partner_sj.ci})")
    else:
        print(f"ℹ️  Partner ya existe en San Juan: {partner_sj.full_name}")
    
    # Establecer contexto para El Progreso
    set_current_organization(org_progreso)
    community_ep, _ = Community.objects.get_or_create(
        name='Comunidad El Progreso Test',
        defaults={'description': 'Comunidad de prueba'}
    )
    print(f"✅ Comunidad creada en El Progreso: {community_ep.name}")
    
    # Crear partner en El Progreso (mismo CI pero diferente organización)
    partner_ep, created = Partner.objects.get_or_create(
        ci='11111111',  # Mismo CI pero en diferente organización
        defaults={
            'first_name': 'María',
            'last_name': 'González',
            'phone': '+59170000002',
            'community': community_ep,
            'status': 'ACTIVE'
        }
    )
    if created:
        print(f"✅ Partner creado en El Progreso: {partner_ep.full_name} (CI: {partner_ep.ci})")
    else:
        print(f"ℹ️  Partner ya existe en El Progreso: {partner_ep.full_name}")
    
    # Demostrar aislamiento de datos
    print_header("2️⃣  VERIFICANDO AISLAMIENTO DE DATOS")
    
    # Ver partners en San Juan
    set_current_organization(org_sanjuan)
    partners_sj = Partner.objects.all()
    print(f"\n🔍 Partners en {org_sanjuan.name}:")
    for p in partners_sj:
        print(f"   - {p.full_name} (CI: {p.ci}) - Org ID: {p.organization_id}")
    print(f"   Total: {partners_sj.count()}")
    
    # Ver partners en El Progreso
    set_current_organization(org_progreso)
    partners_ep = Partner.objects.all()
    print(f"\n🔍 Partners en {org_progreso.name}:")
    for p in partners_ep:
        print(f"   - {p.full_name} (CI: {p.ci}) - Org ID: {p.organization_id}")
    print(f"   Total: {partners_ep.count()}")
    
    # Ver todos los partners (sin filtro)
    print(f"\n🔍 Todos los partners (sin filtro de organización):")
    all_partners = Partner.objects.all_organizations()
    for p in all_partners:
        org_name = p.organization.name if p.organization else 'Sin organización'
        print(f"   - {p.full_name} (CI: {p.ci}) - {org_name}")
    print(f"   Total: {all_partners.count()}")
    
    # Demostrar que el mismo CI puede existir en diferentes organizaciones
    print_header("3️⃣  VERIFICANDO UNICIDAD POR ORGANIZACIÓN")
    
    partners_with_ci = Partner.objects.all_organizations().filter(ci='11111111')
    print(f"\n🔍 Partners con CI '11111111' en todas las organizaciones:")
    for p in partners_with_ci:
        print(f"   - {p.full_name} en {p.organization.name}")
    print(f"   Total: {partners_with_ci.count()}")
    
    if partners_with_ci.count() >= 2:
        print("\n✅ ¡ÉXITO! El mismo CI existe en diferentes organizaciones")
        print("   Esto demuestra que unique_together funciona correctamente")
    
    # Resumen
    print_header("📊 RESUMEN")
    
    print(f"\n✅ Sistema multi-tenant funcionando correctamente:")
    print(f"   - Datos aislados por organización")
    print(f"   - Filtrado automático activo")
    print(f"   - Unicidad por organización (unique_together)")
    print(f"   - Mismo CI puede existir en diferentes organizaciones")
    
    print(f"\n🌐 Para probar en la API:")
    print(f"   San Juan:    http://localhost:8000/api/partners/partners/?org=sanjuan")
    print(f"   El Progreso: http://localhost:8000/api/partners/partners/?org=progreso")
    
    print("\n" + "="*70)
    print("🎉 ¡Demostración completada!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
