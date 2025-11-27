"""
Script para verificar qué organización se está usando actualmente
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from partners.models import Partner

print("📋 Organizaciones en la base de datos:\n")

orgs = Organization.objects.all().order_by('-created_at')

for org in orgs:
    partners_count = Partner.objects.filter(organization=org).count()
    
    print(f"{'='*60}")
    print(f"Nombre: {org.name}")
    print(f"Subdominio: {org.subdomain}")
    print(f"Estado: {org.status}")
    print(f"Creada: {org.created_at}")
    print(f"Socios: {partners_count}")
    print(f"{'='*60}\n")

print("\n💡 Para acceder a una organización específica:")
print("   1. En el navegador, abre DevTools (F12)")
print("   2. Ve a Console")
print("   3. Escribe: localStorage.getItem('currentOrganization')")
print("   4. Verifica qué organización está guardada")
print("\n💡 Para cambiar manualmente:")
print("   localStorage.setItem('currentOrganization', 'SUBDOMINIO')")
print("   location.reload()")
