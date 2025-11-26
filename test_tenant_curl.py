#!/usr/bin/env python
"""Script para probar el header de tenant usando subprocess"""
import subprocess
import json

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
    
    # Comando curl
    cmd = [
        'curl',
        '-s',  # Silent
        '-H', f'X-Organization-Subdomain: {subdomain}',
        '-H', 'Content-Type: application/json',
        f'{API_URL}/api/partners/'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                
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
                elif isinstance(data, dict) and 'error' in data:
                    print(f"❌ Error del servidor: {data.get('error')}")
                    print(f"   Detalle: {data.get('detail', 'N/A')}")
                else:
                    print(f"Respuesta inesperada: {data}")
            except json.JSONDecodeError:
                print(f"❌ Error al parsear JSON")
                print(f"Respuesta: {result.stdout[:200]}")
        else:
            print(f"❌ Error en curl: {result.stderr}")
            
    except FileNotFoundError:
        print("❌ ERROR: curl no está instalado")
        print("   Instala curl o verifica manualmente en el navegador")
        break
    except subprocess.TimeoutExpired:
        print("❌ ERROR: Timeout - el servidor no responde")
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
print("2. O el TenantManager no está filtrando")
print("=" * 80)
