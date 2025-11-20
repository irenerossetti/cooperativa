"""
Script de prueba para verificar que todos los endpoints funcionen correctamente
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    session = requests.Session()
    
    # 1. Test Login
    print("\n🔐 TEST 1: LOGIN")
    response = session.post(f"{BASE_URL}/auth/users/login/", json={
        "username": "admin",
        "password": "admin123"
    })
    print_response("Login", response)
    
    if response.status_code != 200:
        print("❌ Login falló. Verifica las credenciales.")
        return
    
    print("✅ Login exitoso")
    
    # 2. Test GET /api/auth/users/me/
    print("\n👤 TEST 2: GET USUARIO ACTUAL")
    response = session.get(f"{BASE_URL}/auth/users/me/")
    print_response("Usuario Actual", response)
    
    # 3. Test GET /api/auth/users/ (Lista de usuarios)
    print("\n📋 TEST 3: GET LISTA DE USUARIOS")
    response = session.get(f"{BASE_URL}/auth/users/")
    print_response("Lista de Usuarios", response)
    
    # 4. Test GET /api/auth/roles/ (Lista de roles)
    print("\n🎭 TEST 4: GET LISTA DE ROLES")
    response = session.get(f"{BASE_URL}/auth/roles/")
    print_response("Lista de Roles", response)
    
    # 5. Test GET /api/partners/communities/ (Lista de comunidades)
    print("\n🏘️ TEST 5: GET LISTA DE COMUNIDADES")
    response = session.get(f"{BASE_URL}/partners/communities/")
    print_response("Lista de Comunidades", response)
    
    # 6. Test GET /api/partners/partners/ (Lista de socios)
    print("\n👥 TEST 6: GET LISTA DE SOCIOS")
    response = session.get(f"{BASE_URL}/partners/partners/")
    print_response("Lista de Socios", response)
    
    # 7. Test POST /api/partners/partners/ (Crear socio)
    print("\n➕ TEST 7: POST CREAR SOCIO")
    response = session.post(f"{BASE_URL}/partners/partners/", json={
        "ci": "9999999",
        "first_name": "Test",
        "last_name": "Usuario",
        "phone": "+59179999999",
        "community": 1,
        "status": "ACTIVE"
    })
    print_response("Crear Socio", response)
    
    if response.status_code == 201:
        socio_id = response.json()['id']
        print(f"✅ Socio creado con ID: {socio_id}")
        
        # 8. Test GET /api/partners/partners/{id}/ (Detalle de socio)
        print(f"\n🔍 TEST 8: GET DETALLE DE SOCIO (ID: {socio_id})")
        response = session.get(f"{BASE_URL}/partners/partners/{socio_id}/")
        print_response(f"Detalle de Socio {socio_id}", response)
        
        # 9. Test PATCH /api/partners/partners/{id}/ (Actualizar socio)
        print(f"\n✏️ TEST 9: PATCH ACTUALIZAR SOCIO (ID: {socio_id})")
        response = session.patch(f"{BASE_URL}/partners/partners/{socio_id}/", json={
            "phone": "+59179999998"
        })
        print_response(f"Actualizar Socio {socio_id}", response)
    
    # 10. Test GET /api/parcels/soil-types/ (Lista de tipos de suelo)
    print("\n🌱 TEST 10: GET LISTA DE TIPOS DE SUELO")
    response = session.get(f"{BASE_URL}/parcels/soil-types/")
    print_response("Lista de Tipos de Suelo", response)
    
    # 11. Test GET /api/parcels/crops/ (Lista de cultivos)
    print("\n🌾 TEST 11: GET LISTA DE CULTIVOS")
    response = session.get(f"{BASE_URL}/parcels/crops/")
    print_response("Lista de Cultivos", response)
    
    # 12. Test GET /api/parcels/parcels/ (Lista de parcelas)
    print("\n🗺️ TEST 12: GET LISTA DE PARCELAS")
    response = session.get(f"{BASE_URL}/parcels/parcels/")
    print_response("Lista de Parcelas", response)
    
    # 13. Test GET /api/audit/logs/ (Lista de logs de auditoría)
    print("\n📝 TEST 13: GET LISTA DE LOGS DE AUDITORÍA")
    response = session.get(f"{BASE_URL}/audit/logs/")
    print_response("Lista de Logs", response)
    
    # 14. Test Logout
    print("\n🚪 TEST 14: LOGOUT")
    response = session.post(f"{BASE_URL}/auth/users/logout/")
    print_response("Logout", response)
    
    print("\n" + "="*60)
    print("✅ TESTS COMPLETADOS")
    print("="*60)

if __name__ == "__main__":
    print("🚀 Iniciando tests de API...")
    print(f"Base URL: {BASE_URL}")
    print("\n⚠️  Asegúrate de que el servidor esté corriendo:")
    print("   python manage.py runserver")
    
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
