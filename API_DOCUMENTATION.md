# Documentación de API - Sistema de Gestión de Cooperativa

## Autenticación

Todas las peticiones (excepto login) requieren autenticación mediante sesión de Django.

### Login
```http
POST /api/auth/users/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta exitosa:**
```json
{
  "message": "Inicio de sesión exitoso",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@cooperativa.com",
    "first_name": "Admin",
    "last_name": "Sistema",
    "role": 1,
    "role_name": "Administrador",
    "is_active": true
  }
}
```

### Logout
```http
POST /api/auth/users/logout/
```

### Usuario Actual
```http
GET /api/auth/users/me/
```

## Gestión de Usuarios

### Listar Usuarios
```http
GET /api/auth/users/
GET /api/auth/users/?search=juan
GET /api/auth/users/?role=1
GET /api/auth/users/?is_active=true
```

### Crear Usuario
```http
POST /api/auth/users/
Content-Type: application/json

{
  "username": "jperez",
  "email": "jperez@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "phone": "+59170123456",
  "role": 2,
  "password": "Password123!"
}
```

### Actualizar Usuario
```http
PUT /api/auth/users/1/
Content-Type: application/json

{
  "first_name": "Juan Carlos",
  "phone": "+59170123457"
}
```

### Inhabilitar/Reactivar Usuario
```http
POST /api/auth/users/1/deactivate/
POST /api/auth/users/1/activate/
```

## Gestión de Socios

### Listar Socios
```http
GET /api/partners/partners/
GET /api/partners/partners/?search=12345678
GET /api/partners/partners/?community=1
GET /api/partners/partners/?status=ACTIVE
```

**Respuesta:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "ci": "12345678",
      "full_name": "Juan Pérez",
      "phone": "+59170123456",
      "community_name": "Comunidad San José",
      "status": "ACTIVE",
      "status_display": "Activo"
    }
  ]
}
```

### Crear Socio
```http
POST /api/partners/partners/
Content-Type: application/json

{
  "ci": "12345678",
  "nit": "1234567890",
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan@example.com",
  "phone": "+59170123456",
  "address": "Calle Principal #123",
  "community": 1,
  "status": "ACTIVE",
  "notes": "Socio fundador"
}
```

### Detalle de Socio
```http
GET /api/partners/partners/1/
```

**Respuesta:**
```json
{
  "id": 1,
  "ci": "12345678",
  "nit": "1234567890",
  "first_name": "Juan",
  "last_name": "Pérez",
  "full_name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+59170123456",
  "address": "Calle Principal #123",
  "community": 1,
  "community_name": "Comunidad San José",
  "user": null,
  "status": "ACTIVE",
  "status_display": "Activo",
  "registration_date": "2025-11-20",
  "notes": "Socio fundador",
  "total_parcels": 2,
  "total_surface": "15.50",
  "created_at": "2025-11-20T18:00:00Z",
  "updated_at": "2025-11-20T18:00:00Z"
}
```

### Actualizar Socio
```http
PUT /api/partners/partners/1/
PATCH /api/partners/partners/1/
Content-Type: application/json

{
  "phone": "+59170999999",
  "address": "Nueva dirección"
}
```

### Cambiar Estado de Socio
```http
POST /api/partners/partners/1/deactivate/
POST /api/partners/partners/1/activate/
POST /api/partners/partners/1/suspend/
```

## Gestión de Comunidades

### Listar Comunidades
```http
GET /api/partners/communities/
GET /api/partners/communities/?is_active=true
```

### Crear Comunidad
```http
POST /api/partners/communities/
Content-Type: application/json

{
  "name": "Comunidad Nueva",
  "description": "Descripción de la comunidad",
  "is_active": true
}
```

## Gestión de Parcelas

### Listar Parcelas
```http
GET /api/parcels/parcels/
GET /api/parcels/parcels/?partner=1
GET /api/parcels/parcels/?soil_type=1
GET /api/parcels/parcels/?crop=1
GET /api/parcels/parcels/?status=ACTIVE
GET /api/parcels/parcels/?search=P001
```

### Crear Parcela
```http
POST /api/parcels/parcels/
Content-Type: application/json

{
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
  "notes": "Parcela con riego"
}
```

### Detalle de Parcela
```http
GET /api/parcels/parcels/1/
```

**Respuesta:**
```json
{
  "id": 1,
  "code": "P001",
  "name": "Parcela Norte",
  "surface": "5.50",
  "location": "Sector Norte, Lote 1",
  "latitude": "-17.3935000",
  "longitude": "-66.1570000",
  "partner": 1,
  "partner_name": "Juan Pérez",
  "soil_type": 1,
  "soil_type_name": "Arcilloso",
  "current_crop": 1,
  "crop_name": "Café",
  "status": "ACTIVE",
  "status_display": "Activa",
  "notes": "Parcela con riego",
  "created_at": "2025-11-20T18:00:00Z",
  "updated_at": "2025-11-20T18:00:00Z"
}
```

## Tipos de Suelo y Cultivos

### Listar Tipos de Suelo
```http
GET /api/parcels/soil-types/
```

### Listar Cultivos
```http
GET /api/parcels/crops/
```

## Auditoría

### Listar Registros de Auditoría
```http
GET /api/audit/logs/
GET /api/audit/logs/?user=1
GET /api/audit/logs/?action=LOGIN
GET /api/audit/logs/?model_name=Partner
GET /api/audit/logs/?date_from=2025-11-01
GET /api/audit/logs/?date_to=2025-11-30
GET /api/audit/logs/?search=juan
```

**Respuesta:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "username": "admin",
      "action": "LOGIN",
      "action_display": "Inicio de sesión",
      "model_name": "User",
      "object_id": 1,
      "description": "Usuario admin inició sesión",
      "ip_address": "127.0.0.1",
      "timestamp": "2025-11-20T18:00:00Z"
    }
  ]
}
```

## Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `400 Bad Request` - Error en los datos enviados
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - Sin permisos
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

## Validaciones

### Usuarios
- Username único
- Email único y válido
- Contraseña con validación de seguridad

### Socios
- CI único (7-10 dígitos)
- NIT único (7-15 dígitos)
- Email válido
- Teléfono en formato internacional

### Parcelas
- Código único
- Superficie mayor a 0
- Socio debe existir

## Paginación

Todas las listas están paginadas con 25 elementos por página.

```http
GET /api/partners/partners/?page=2
GET /api/partners/partners/?page_size=50
```

## Roles y Permisos

### Administrador (ADMIN)
- Acceso completo a todas las funcionalidades

### Socio (PARTNER)
- Solo lectura de socios y parcelas

### Operador (OPERATOR)
- Crear, leer y actualizar socios y parcelas
- No puede eliminar
