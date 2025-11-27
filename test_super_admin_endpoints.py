"""
Script para probar los endpoints del super admin
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

# Primero hacer login como superadmin
session = requests.Session()

# Login
login_data = {
    'username': 'superadmin',
    'password': 'admin123'
}

print("1. Haciendo login como superadmin...")
response = session.post(f'{BASE_URL}/api/auth/users/login/', json=login_data)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✅ Login exitoso")
    user_data = response.json()
    print(f"   Usuario: {user_data.get('user', {}).get('username')}")
    print(f"   Superuser: {user_data.get('user', {}).get('is_superuser')}")
else:
    print(f"   ❌ Error: {response.text}")
    exit(1)

print("\n2. Obteniendo estadísticas...")
response = session.get(f'{BASE_URL}/api/tenants/super-admin/stats/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    stats = response.json()
    print(f"   ✅ Total organizaciones: {stats['organizations']['total']}")
    print(f"   ✅ Organizaciones activas: {stats['organizations']['active']}")
else:
    print(f"   ❌ Error: {response.text}")

print("\n3. Listando organizaciones...")
response = session.get(f'{BASE_URL}/api/tenants/super-admin/organizations/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    orgs = response.json()
    print(f"   ✅ Encontradas {len(orgs)} organizaciones")
    if orgs:
        org_id = orgs[0]['id']
        org_name = orgs[0]['name']
        print(f"   Primera organización: {org_name} (ID: {org_id})")
        
        print(f"\n4. Obteniendo detalles de '{org_name}'...")
        response = session.get(f'{BASE_URL}/api/tenants/super-admin/organizations/{org_id}/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Detalles obtenidos correctamente")
        else:
            print(f"   ❌ Error: {response.text}")
        
        # Probar delete (comentado para no eliminar accidentalmente)
        print(f"\n5. Probando endpoint de delete (sin ejecutar)...")
        print(f"   URL: {BASE_URL}/api/tenants/super-admin/organizations/{org_id}/delete/")
        print(f"   Método: DELETE")
        print(f"   ⚠️  Para probar, descomenta la línea en el script")
        
        # Descomentar para probar delete:
        # response = session.delete(f'{BASE_URL}/api/tenants/super-admin/organizations/{org_id}/delete/')
        # print(f"   Status: {response.status_code}")
        # print(f"   Response: {response.text}")
else:
    print(f"   ❌ Error: {response.text}")

print("\n✅ Pruebas completadas")
