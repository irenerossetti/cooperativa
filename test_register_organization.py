import requests
import json

print("=" * 60)
print("PRUEBA DE REGISTRO DE ORGANIZACIÓN")
print("=" * 60)

# URL del endpoint
url = "http://localhost:8000/api/tenants/register/"

# Datos de la nueva organización
data = {
    "organization_name": "Cooperativa Prueba API",
    "subdomain": "pruebaapi",
    "email": "contacto@pruebaapi.com",
    "phone": "+591 3 9876543",
    "username": "adminprueba",
    "user_email": "admin@pruebaapi.com",
    "password": "password123",
    "first_name": "Admin",
    "last_name": "Prueba"
}

print("\n📤 Enviando solicitud de registro...")
print(f"URL: {url}")
print(f"Datos: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data)
    
    print(f"\n📥 Respuesta recibida:")
    print(f"Status Code: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("\n✅ ¡Organización registrada exitosamente!")
        result = response.json()
        print(f"\n📋 Detalles:")
        print(f"   Organización: {result['organization']['name']}")
        print(f"   Subdominio: {result['organization']['subdomain']}")
        print(f"   Plan: {result['organization']['plan']}")
        print(f"   Usuario: {result['user']['username']}")
        print(f"\n🔗 Puedes acceder con:")
        print(f"   - http://localhost:8000/api/partners/?org={result['organization']['subdomain']}")
        print(f"   - Header: X-Organization-Subdomain: {result['organization']['subdomain']}")
    else:
        print("\n❌ Error al registrar organización")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Error: No se pudo conectar al servidor")
    print("   Asegúrate de que el servidor esté corriendo:")
    print("   python manage.py runserver")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "=" * 60)
