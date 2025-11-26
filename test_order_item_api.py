import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sales.models import Order
from production.models import HarvestedProduct

print("=" * 60)
print("PROBANDO API DE ORDER ITEMS")
print("=" * 60)

# Obtener datos necesarios
order = Order.objects.filter(status='DRAFT').first()
product = HarvestedProduct.objects.filter(product_name__icontains='semilla').first()

if not order or not product:
    print("❌ No hay datos de prueba disponibles")
    exit(1)

print(f"✅ Pedido: {order.order_number} (ID: {order.id})")
print(f"✅ Producto: {product.product_name} (ID: {product.id})")

# Datos para enviar
data = {
    'order': order.id,
    'product': product.id,
    'quantity': 5.0,
    'unit_price': 250.0
}

print(f"\n📤 Enviando datos:")
print(json.dumps(data, indent=2))

# Hacer la petición
url = 'http://localhost:8000/api/sales/order-items/'
headers = {
    'Content-Type': 'application/json',
}

# Primero necesitamos autenticarnos
# Obtener token de un usuario
from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.filter(is_active=True).first()
if not user:
    print("❌ No hay usuarios activos")
    exit(1)

# Usar autenticación básica o session
# Para simplificar, vamos a hacer login primero
session = requests.Session()
login_url = 'http://localhost:8000/api/users/login/'
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

login_response = session.post(login_url, json=login_data)
if login_response.status_code == 200:
    token_data = login_response.json()
    if 'token' in token_data:
        headers['Authorization'] = f'Token {token_data["token"]}'
        print(f"\n🔑 Autenticado como: admin")
    else:
        print("❌ No se pudo obtener el token")
        exit(1)
else:
    print(f"❌ Error en login: {login_response.status_code}")
    print(login_response.text)
    exit(1)

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"\n📥 Respuesta: {response.status_code}")
    print(f"Contenido: {response.text}")
    
    if response.status_code == 201:
        print("\n✅ ¡OrderItem creado exitosamente!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\n❌ Error al crear OrderItem")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
            
except Exception as e:
    print(f"❌ Error en la petición: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
