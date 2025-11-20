# Ejemplos de Uso de la API

## Flujo Completo de Uso

### 1. Iniciar Sesión

```bash
curl -X POST http://localhost:8000/api/auth/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }' \
  -c cookies.txt
```

### 2. Crear una Comunidad

```bash
curl -X POST http://localhost:8000/api/partners/communities/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Comunidad Los Pinos",
    "description": "Comunidad ubicada en la zona oeste",
    "is_active": true
  }'
```

### 3. Crear un Socio

```bash
curl -X POST http://localhost:8000/api/partners/partners/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "ci": "7654321",
    "nit": "7654321012",
    "first_name": "María",
    "last_name": "González",
    "email": "maria@example.com",
    "phone": "+59171234567",
    "address": "Av. Principal #456",
    "community": 1,
    "status": "ACTIVE",
    "notes": "Socia desde 2020"
  }'
```

### 4. Crear una Parcela para el Socio

```bash
curl -X POST http://localhost:8000/api/parcels/parcels/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "code": "P001",
    "name": "Parcela El Rosal",
    "surface": 8.5,
    "location": "Sector Norte, Lote 5",
    "latitude": -17.3935,
    "longitude": -66.1570,
    "partner": 1,
    "soil_type": 1,
    "current_crop": 1,
    "status": "ACTIVE",
    "notes": "Parcela con sistema de riego por goteo"
  }'
```

### 5. Buscar Socios por Comunidad

```bash
curl -X GET "http://localhost:8000/api/partners/partners/?community=1" \
  -b cookies.txt
```

### 6. Buscar Parcelas por Socio

```bash
curl -X GET "http://localhost:8000/api/parcels/parcels/?partner=1" \
  -b cookies.txt
```

### 7. Ver Detalle de un Socio

```bash
curl -X GET http://localhost:8000/api/partners/partners/1/ \
  -b cookies.txt
```

### 8. Actualizar Información de un Socio

```bash
curl -X PATCH http://localhost:8000/api/partners/partners/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "phone": "+59171999999",
    "address": "Nueva dirección #789"
  }'
```

### 9. Inhabilitar un Socio

```bash
curl -X POST http://localhost:8000/api/partners/partners/1/deactivate/ \
  -b cookies.txt
```

### 10. Ver Registros de Auditoría

```bash
curl -X GET "http://localhost:8000/api/audit/logs/?action=LOGIN" \
  -b cookies.txt
```

### 11. Crear un Usuario Operador

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "username": "operador1",
    "email": "operador1@cooperativa.com",
    "first_name": "Carlos",
    "last_name": "Ramírez",
    "phone": "+59172345678",
    "role": 3,
    "password": "Operador123!"
  }'
```

### 12. Cerrar Sesión

```bash
curl -X POST http://localhost:8000/api/auth/users/logout/ \
  -b cookies.txt
```

## Ejemplos con Python (requests)

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# Crear sesión
session = requests.Session()

# 1. Login
login_data = {
    "username": "admin",
    "password": "admin123"
}
response = session.post(f"{BASE_URL}/auth/users/login/", json=login_data)
print("Login:", response.json())

# 2. Listar socios
response = session.get(f"{BASE_URL}/partners/partners/")
print("Socios:", response.json())

# 3. Crear socio
socio_data = {
    "ci": "8765432",
    "first_name": "Pedro",
    "last_name": "López",
    "phone": "+59173456789",
    "community": 1,
    "status": "ACTIVE"
}
response = session.post(f"{BASE_URL}/partners/partners/", json=socio_data)
print("Socio creado:", response.json())

# 4. Buscar socios por nombre
response = session.get(f"{BASE_URL}/partners/partners/?search=Pedro")
print("Búsqueda:", response.json())

# 5. Ver logs de auditoría
response = session.get(f"{BASE_URL}/audit/logs/")
print("Auditoría:", response.json())

# 6. Logout
response = session.post(f"{BASE_URL}/auth/users/logout/")
print("Logout:", response.json())
```

## Ejemplos con JavaScript (fetch)

```javascript
// Base URL
const BASE_URL = 'http://localhost:8000/api';

// 1. Login
async function login() {
  const response = await fetch(`${BASE_URL}/auth/users/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Para incluir cookies
    body: JSON.stringify({
      username: 'admin',
      password: 'admin123'
    })
  });
  const data = await response.json();
  console.log('Login:', data);
}

// 2. Listar socios
async function listarSocios() {
  const response = await fetch(`${BASE_URL}/partners/partners/`, {
    credentials: 'include'
  });
  const data = await response.json();
  console.log('Socios:', data);
}

// 3. Crear socio
async function crearSocio() {
  const response = await fetch(`${BASE_URL}/partners/partners/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      ci: '9876543',
      first_name: 'Ana',
      last_name: 'Martínez',
      phone: '+59174567890',
      community: 1,
      status: 'ACTIVE'
    })
  });
  const data = await response.json();
  console.log('Socio creado:', data);
}

// 4. Buscar socios
async function buscarSocios(termino) {
  const response = await fetch(
    `${BASE_URL}/partners/partners/?search=${termino}`,
    { credentials: 'include' }
  );
  const data = await response.json();
  console.log('Búsqueda:', data);
}

// 5. Logout
async function logout() {
  const response = await fetch(`${BASE_URL}/auth/users/logout/`, {
    method: 'POST',
    credentials: 'include'
  });
  const data = await response.json();
  console.log('Logout:', data);
}

// Ejecutar
login()
  .then(() => listarSocios())
  .then(() => crearSocio())
  .then(() => buscarSocios('Ana'))
  .then(() => logout());
```

## Casos de Uso Comunes

### Caso 1: Registrar un nuevo socio con su parcela

```python
import requests

session = requests.Session()
BASE_URL = "http://localhost:8000/api"

# Login
session.post(f"{BASE_URL}/auth/users/login/", json={
    "username": "admin",
    "password": "admin123"
})

# Crear socio
socio = session.post(f"{BASE_URL}/partners/partners/", json={
    "ci": "1234567",
    "first_name": "Roberto",
    "last_name": "Silva",
    "phone": "+59175678901",
    "community": 1,
    "status": "ACTIVE"
}).json()

socio_id = socio['id']

# Crear parcela para el socio
parcela = session.post(f"{BASE_URL}/parcels/parcels/", json={
    "code": f"P{socio_id:03d}",
    "name": f"Parcela de {socio['full_name']}",
    "surface": 10.0,
    "location": "Sector Sur",
    "partner": socio_id,
    "soil_type": 1,
    "current_crop": 1,
    "status": "ACTIVE"
}).json()

print(f"Socio {socio['full_name']} registrado con parcela {parcela['code']}")
```

### Caso 2: Listar todos los socios de una comunidad con sus parcelas

```python
# Obtener socios de la comunidad 1
socios = session.get(f"{BASE_URL}/partners/partners/?community=1").json()

for socio in socios['results']:
    print(f"\nSocio: {socio['full_name']}")
    
    # Obtener parcelas del socio
    parcelas = session.get(
        f"{BASE_URL}/parcels/parcels/?partner={socio['id']}"
    ).json()
    
    print(f"  Parcelas: {parcelas['count']}")
    for parcela in parcelas['results']:
        print(f"    - {parcela['code']}: {parcela['surface']} ha")
```

### Caso 3: Generar reporte de auditoría de un usuario

```python
# Ver todas las acciones de un usuario
user_id = 1
logs = session.get(f"{BASE_URL}/audit/logs/?user={user_id}").json()

print(f"Acciones del usuario {user_id}:")
for log in logs['results']:
    print(f"  {log['timestamp']}: {log['action_display']} - {log['description']}")
```

## Respuestas de Error Comunes

### Error 400 - Datos inválidos
```json
{
  "ci": ["Este CI ya está registrado."],
  "email": ["Formato de email inválido."]
}
```

### Error 401 - No autenticado
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Error 403 - Sin permisos
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Error 404 - No encontrado
```json
{
  "detail": "Not found."
}
```
