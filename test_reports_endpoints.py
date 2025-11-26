"""
Script para probar los endpoints de reportes
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

# Primero hacer login para obtener el token
def login():
    response = requests.post(f'{BASE_URL}/api/users/login/', json={
        'username': 'admin',
        'password': 'admin123'
    })
    if response.status_code == 200:
        data = response.json()
        return data.get('access')
    return None

def test_endpoints(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'X-Organization': 'cooperativa-demo'
    }
    
    endpoints = [
        '/api/reports/reports/partners_by_community/',
        '/api/reports/reports/hectares_by_crop/',
        '/api/reports/reports/fertilization_plan/',
        '/api/reports/reports/price_alerts/',
    ]
    
    print("🧪 Probando endpoints de reportes...\n")
    
    for endpoint in endpoints:
        print(f"📍 Probando: {endpoint}")
        try:
            response = requests.get(f'{BASE_URL}{endpoint}', headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Respuesta exitosa")
                print(f"   Datos: {json.dumps(data, indent=2)[:200]}...")
            else:
                print(f"   ❌ Error: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Excepción: {str(e)}")
        print()

if __name__ == '__main__':
    print("🚀 Iniciando pruebas de endpoints...\n")
    
    token = login()
    if token:
        print(f"✅ Login exitoso\n")
        test_endpoints(token)
    else:
        print("❌ Error en login")
