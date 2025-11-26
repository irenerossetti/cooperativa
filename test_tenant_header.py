#!/usr/bin/env python
"""Script para simular requests con diferentes headers de organización"""
import requests

API_URL = "http://localhost:8000"

print("=" * 80)
print("PRUEBA: VERIFICANDO SI EL BACKEND RESPETA EL HEADER X-Organization-Subdomain")
print("=" * 80)

# Organizaciones a probar
orgs_to_test = [
    ('sanjuan', 'Cooperativa San Juan'),
    ('progreso', 'Cooperativa El Progreso'),
    ('demo', 'Cooperativa Demo'),
]

print("\n🔍 Probando endpoint /api/partners/ con diferentes headers...\n")

for subdomain, name in orgs_to_test:
    print(f"\n{'='*80}")
    print(f"📍 Probando: {name} (subdomain: {subdomain})")
    print(f"{'='*80}")
    
    headers = {
        'X-Organization-Subdomain': subdomain,
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.get(
            f"{API_URL}/api/partners/",
            headers=headers,
            timeout=5
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, list):
                count = len(data)
                print(f"✅ Partners encontrados: {count}")
                
                if count > 0:
                    print(f"\nPrimeros 3 partners:")
                    for partner in data[:3]:
                        name_partner = f"{partner.get('first_name', '')} {partner.get('last_name', '')}"
                        ci = partner.get('ci', 'N/A')
                        print(f"   - {name_partner} (CI: {ci})")
                else:
                    print("   (Sin partners)")
            else:
                print(f"Respuesta: {data}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor Django está corriendo en http://localhost:8000")
        break
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("CONCLUSIÓN:")
print("=" * 80)
print("Si ves diferentes cantidades de partners para cada organización,")
print("entonces el backend SÍ está respetando el header.")
print("\nSi ves la misma cantidad en todas, el problema es que:")
print("1. El middleware no está procesando el header correctamente")
print("2. O el frontend no está enviando el header")
print("=" * 80)
