# Endpoints Disponibles - API REST

## 🔐 Autenticación

### Login
```
POST /api/auth/users/login/
Body: {"username": "admin", "password": "admin123"}
```

### Logout
```
POST /api/auth/users/logout/
```

### Usuario Actual
```
GET /api/auth/users/me/
```

### Cambiar Contraseña
```
POST /api/auth/users/change_password/
Body: {"old_password": "...", "new_password": "..."}
```

---

## 👥 Usuarios

### Listar Usuarios (GET ALL)
```
GET /api/auth/users/
GET /api/auth/users/?search=juan
GET /api/auth/users/?role=1
GET /api/auth/users/?is_active=true
GET /api/auth/users/?page=2
```

### Obtener Usuario por ID (GET BY ID)
```
GET /api/auth/users/1/
GET /api/auth/users/2/
```

### Crear Usuario
```
POST /api/auth/users/
Body: {
  "username": "nuevo_usuario",
  "email": "usuario@example.com",
  "first_name": "Nombre",
  "last_name": "Apellido",
  "phone": "+59170123456",
  "role": 2,
  "password": "Password123!"
}
```

### Actualizar Usuario
```
PUT /api/auth/users/1/
PATCH /api/auth/users/1/
Body: {"first_name": "Nuevo Nombre"}
```

### Eliminar Usuario
```
DELETE /api/auth/users/1/
```

### Acciones Especiales
```
POST /api/auth/users/1/deactivate/
POST /api/auth/users/1/activate/
```

---

## 🎭 Roles

### Listar Roles (GET ALL)
```
GET /api/auth/roles/
GET /api/auth/roles/?is_active=true
```

### Obtener Rol por ID (GET BY ID)
```
GET /api/auth/roles/1/
```

### Crear Rol
```
POST /api/auth/roles/
Body: {
  "name": "CUSTOM",
  "description": "Rol personalizado",
  "permissions": {},
  "is_active": true
}
```

### Actualizar Rol
```
PUT /api/auth/roles/1/
PATCH /api/auth/roles/1/
```

### Eliminar Rol
```
DELETE /api/auth/roles/1/
```

---

## 🏘️ Comunidades

### Listar Comunidades (GET ALL)
```
GET /api/partners/communities/
GET /api/partners/communities/?is_active=true
```

### Obtener Comunidad por ID (GET BY ID)
```
GET /api/partners/communities/1/
```

### Crear Comunidad
```
POST /api/partners/communities/
Body: {
  "name": "Nueva Comunidad",
  "description": "Descripción",
  "is_active": true
}
```

### Actualizar Comunidad
```
PUT /api/partners/communities/1/
PATCH /api/partners/communities/1/
```

### Eliminar Comunidad
```
DELETE /api/partners/communities/1/
```

---

## 👨‍🌾 Socios

### Listar Socios (GET ALL)
```
GET /api/partners/partners/
GET /api/partners/partners/?search=12345678
GET /api/partners/partners/?community=1
GET /api/partners/partners/?status=ACTIVE
GET /api/partners/partners/?page=2
GET /api/partners/partners/?page_size=50
```

### Obtener Socio por ID (GET BY ID)
```
GET /api/partners/partners/1/
GET /api/partners/partners/2/
```

### Crear Socio
```
POST /api/partners/partners/
Body: {
  "ci": "12345678",
  "nit": "1234567890",
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan@example.com",
  "phone": "+59170123456",
  "address": "Calle Principal #123",
  "community": 1,
  "status": "ACTIVE",
  "notes": "Notas opcionales"
}
```

### Actualizar Socio
```
PUT /api/partners/partners/1/
PATCH /api/partners/partners/1/
Body: {"phone": "+59170999999"}
```

### Eliminar Socio
```
DELETE /api/partners/partners/1/
```

### Acciones Especiales
```
POST /api/partners/partners/1/deactivate/
POST /api/partners/partners/1/activate/
POST /api/partners/partners/1/suspend/
```

---

## 🌱 Tipos de Suelo

### Listar Tipos de Suelo (GET ALL)
```
GET /api/parcels/soil-types/
```

### Obtener Tipo de Suelo por ID (GET BY ID)
```
GET /api/parcels/soil-types/1/
```

### Crear Tipo de Suelo
```
POST /api/parcels/soil-types/
Body: {
  "name": "Limoso",
  "description": "Suelo con buena retención de nutrientes",
  "is_active": true
}
```

### Actualizar Tipo de Suelo
```
PUT /api/parcels/soil-types/1/
PATCH /api/parcels/soil-types/1/
```

### Eliminar Tipo de Suelo
```
DELETE /api/parcels/soil-types/1/
```

---

## 🌾 Cultivos

### Listar Cultivos (GET ALL)
```
GET /api/parcels/crops/
```

### Obtener Cultivo por ID (GET BY ID)
```
GET /api/parcels/crops/1/
```

### Crear Cultivo
```
POST /api/parcels/crops/
Body: {
  "name": "Quinua",
  "scientific_name": "Chenopodium quinoa",
  "description": "Pseudocereal andino",
  "is_active": true
}
```

### Actualizar Cultivo
```
PUT /api/parcels/crops/1/
PATCH /api/parcels/crops/1/
```

### Eliminar Cultivo
```
DELETE /api/parcels/crops/1/
```

---

## 🗺️ Parcelas

### Listar Parcelas (GET ALL)
```
GET /api/parcels/parcels/
GET /api/parcels/parcels/?partner=1
GET /api/parcels/parcels/?soil_type=1
GET /api/parcels/parcels/?crop=1
GET /api/parcels/parcels/?status=ACTIVE
GET /api/parcels/parcels/?search=P001
```

### Obtener Parcela por ID (GET BY ID)
```
GET /api/parcels/parcels/1/
```

### Crear Parcela
```
POST /api/parcels/parcels/
Body: {
  "code": "P001",
  "name": "Parcela Norte",
  "surface": 5.5,
  "location": "Sector Norte, Lote 1",
  "latitude": -17.3935,
  "longitude": -66.1570,
  "partner": 1,
  "soil_type": 1,
  "current_crop": 1,
  "status": "ACTIVE",
  "notes": "Notas opcionales"
}
```

### Actualizar Parcela
```
PUT /api/parcels/parcels/1/
PATCH /api/parcels/parcels/1/
Body: {"surface": 6.0}
```

### Eliminar Parcela
```
DELETE /api/parcels/parcels/1/
```

---

## 📝 Auditoría

### Listar Logs de Auditoría (GET ALL)
```
GET /api/audit/logs/
GET /api/audit/logs/?user=1
GET /api/audit/logs/?action=LOGIN
GET /api/audit/logs/?model_name=Partner
GET /api/audit/logs/?date_from=2025-11-01
GET /api/audit/logs/?date_to=2025-11-30
GET /api/audit/logs/?search=admin
```

### Obtener Log por ID (GET BY ID)
```
GET /api/audit/logs/1/
```

**Nota:** Los logs de auditoría son de solo lectura (no se pueden crear, actualizar o eliminar manualmente).

---

## 📊 Resumen de Métodos HTTP

| Método | Acción | Ejemplo |
|--------|--------|---------|
| GET | Listar todos (sin ID) | `GET /api/partners/partners/` |
| GET | Obtener uno (con ID) | `GET /api/partners/partners/1/` |
| POST | Crear | `POST /api/partners/partners/` |
| PUT | Actualizar completo | `PUT /api/partners/partners/1/` |
| PATCH | Actualizar parcial | `PATCH /api/partners/partners/1/` |
| DELETE | Eliminar | `DELETE /api/partners/partners/1/` |

---

## 🧪 Probar con cURL

### Ejemplo completo:

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' \
  -c cookies.txt

# 2. Listar socios (GET ALL)
curl -X GET http://localhost:8000/api/partners/partners/ \
  -b cookies.txt

# 3. Obtener socio por ID (GET BY ID)
curl -X GET http://localhost:8000/api/partners/partners/1/ \
  -b cookies.txt

# 4. Crear socio
curl -X POST http://localhost:8000/api/partners/partners/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "ci": "7654321",
    "first_name": "María",
    "last_name": "González",
    "phone": "+59171234567",
    "community": 1,
    "status": "ACTIVE"
  }'

# 5. Actualizar socio
curl -X PATCH http://localhost:8000/api/partners/partners/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"phone": "+59171999999"}'

# 6. Logout
curl -X POST http://localhost:8000/api/auth/users/logout/ \
  -b cookies.txt
```

---

## 🔍 Verificar que el servidor esté corriendo

```bash
# Iniciar servidor
python manage.py runserver

# Probar endpoint básico
curl http://localhost:8000/api/auth/roles/
```

Si ves un error de autenticación, primero haz login y guarda las cookies.

---

## 📱 Probar con Postman

1. Importa la colección (si existe `Postman_Collection.json`)
2. Configura la variable `base_url` = `http://localhost:8000/api`
3. Ejecuta primero el request de Login
4. Las cookies se guardarán automáticamente
5. Prueba los demás endpoints

---

## ✅ Endpoints Confirmados

Todos los ViewSets de Django REST Framework incluyen automáticamente:

- ✅ `list()` - GET /resource/ (listar todos)
- ✅ `retrieve()` - GET /resource/{id}/ (obtener uno)
- ✅ `create()` - POST /resource/ (crear)
- ✅ `update()` - PUT /resource/{id}/ (actualizar completo)
- ✅ `partial_update()` - PATCH /resource/{id}/ (actualizar parcial)
- ✅ `destroy()` - DELETE /resource/{id}/ (eliminar)

Más acciones personalizadas con `@action` decorator.
