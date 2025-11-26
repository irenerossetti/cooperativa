# API de Auditoría - Ejemplos de Uso

## 🔐 Autenticación Requerida

Todos los endpoints requieren:
- **Autenticación:** Usuario autenticado
- **Permisos:** Rol de Administrador
- **Header:** `X-Organization-Subdomain` (para multi-tenancy)

---

## 📋 Endpoints Disponibles

### 1. Listar Todos los Logs (Con Restricción de Organización)

```bash
GET /api/audit/
```

**Headers:**
```
Authorization: Basic <credentials>
X-Organization-Subdomain: mi-organizacion
```

**Respuesta:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/audit/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 5,
      "username": "juan.perez",
      "action": "LOGIN",
      "action_display": "Inicio de sesión",
      "model_name": "",
      "object_id": null,
      "description": "Usuario inició sesión exitosamente",
      "ip_address": "192.168.1.100",
      "timestamp": "2025-11-26T10:30:45.123456-04:00"
    },
    {
      "id": 2,
      "user": 5,
      "username": "juan.perez",
      "action": "CREATE",
      "action_display": "Creación",
      "model_name": "Product",
      "object_id": 15,
      "description": "Creó producto: Fertilizante NPK 20-20-20",
      "ip_address": "192.168.1.100",
      "timestamp": "2025-11-26T10:35:12.789012-04:00"
    }
  ]
}
```

---

### 2. Filtrar por Usuario

```bash
GET /api/audit/?user=5
```

**Ejemplo con curl:**
```bash
curl -X GET "http://localhost:8000/api/audit/?user=5" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -H "X-Organization-Subdomain: mi-organizacion"
```

---

### 3. Filtrar por Tipo de Acción

```bash
GET /api/audit/?action=LOGIN
```

**Acciones disponibles:**
- `LOGIN` - Inicio de sesión
- `LOGOUT` - Cierre de sesión
- `LOGIN_FAILED` - Intento fallido
- `CREATE` - Creación
- `UPDATE` - Actualización
- `DELETE` - Eliminación

**Ejemplo:**
```bash
curl -X GET "http://localhost:8000/api/audit/?action=LOGIN_FAILED" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -H "X-Organization-Subdomain: mi-organizacion"
```

---

### 4. Filtrar por Modelo

```bash
GET /api/audit/?model_name=Product
```

**Ejemplo:**
```bash
curl -X GET "http://localhost:8000/api/audit/?model_name=Partner" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -H "X-Organization-Subdomain: mi-organizacion"
```

---

### 5. Filtrar por Rango de Fechas

```bash
GET /api/audit/?date_from=2025-11-01&date_to=2025-11-30
```

**Ejemplo:**
```bash
curl -X GET "http://localhost:8000/api/audit/?date_from=2025-11-01T00:00:00&date_to=2025-11-30T23:59:59" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -H "X-Organization-Subdomain: mi-organizacion"
```

---

### 6. Búsqueda por Texto

```bash
GET /api/audit/?search=fertilizante
```

Busca en:
- Descripción del log
- Nombre de usuario

**Ejemplo:**
```bash
curl -X GET "http://localhost:8000/api/audit/?search=eliminó" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -H "X-Organization-Subdomain: mi-organizacion"
```

---

### 7. Combinar Múltiples Filtros

```bash
GET /api/audit/?user=5&action=CREATE&date_from=2025-11-01
```

**Ejemplo:**
```bash
curl -X GET "http://localhost:8000/api/audit/?user=5&action=CREATE&model_name=Product&date_from=2025-11-01" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -H "X-Organization-Subdomain: mi-organizacion"
```

---

## 🔑 Acceso con Llave de Desarrollador

### Endpoint Especial (Sin Restricciones de Organización)

```bash
GET /api/audit/developer-access/
```

**⚠️ IMPORTANTE:** Este endpoint:
- NO requiere autenticación de usuario
- NO tiene restricciones de organización
- Muestra logs de TODAS las organizaciones
- Requiere llave secreta de desarrollador

**Headers Requeridos:**
```
X-Developer-Key: tu-llave-secreta-unica-aqui
```

**Ejemplo:**
```bash
curl -X GET "http://localhost:8000/api/audit/developer-access/" \
  -H "X-Developer-Key: tu-llave-secreta-unica-aqui"
```

**Respuesta:**
```json
{
  "message": "Acceso de desarrollador autorizado",
  "total_records": 500,
  "results": [
    {
      "id": 1,
      "user": 5,
      "username": "juan.perez",
      "action": "LOGIN",
      "action_display": "Inicio de sesión",
      "model_name": "",
      "object_id": null,
      "description": "Usuario inició sesión exitosamente",
      "ip_address": "192.168.1.100",
      "timestamp": "2025-11-26T10:30:45.123456-04:00"
    }
  ]
}
```

---

### Filtros Disponibles con Llave de Desarrollador

```bash
# Filtrar por usuario
GET /api/audit/developer-access/?user=5

# Filtrar por acción
GET /api/audit/developer-access/?action=LOGIN

# Filtrar por organización específica
GET /api/audit/developer-access/?organization=1

# Combinar filtros
GET /api/audit/developer-access/?user=5&action=CREATE&organization=2
```

**Ejemplo completo:**
```bash
curl -X GET "http://localhost:8000/api/audit/developer-access/?organization=1&action=LOGIN_FAILED" \
  -H "X-Developer-Key: tu-llave-secreta-unica-aqui"
```

---

## 🚫 Errores Comunes

### Error 401: No Autenticado
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Solución:** Agregar header de autenticación

---

### Error 403: Sin Permisos
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**Solución:** El usuario debe tener rol de Administrador

---

### Error 403: Llave de Desarrollador Inválida
```json
{
  "error": "Acceso denegado",
  "detail": "Llave de desarrollador inválida o no proporcionada"
}
```

**Solución:** Verificar que la llave en el header coincida con `AUDIT_DEVELOPER_KEY` en `.env`

---

### Error 503: Llave No Configurada
```json
{
  "error": "Sistema de llave de desarrollador no configurado",
  "detail": "Configure AUDIT_DEVELOPER_KEY en variables de entorno"
}
```

**Solución:** Agregar `AUDIT_DEVELOPER_KEY` en el archivo `.env`

---

## 📊 Ejemplos con Python Requests

### Consulta Normal (Con Autenticación)

```python
import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:8000/api/audit/"
headers = {
    "X-Organization-Subdomain": "mi-organizacion"
}
auth = HTTPBasicAuth('admin', 'password')

response = requests.get(url, headers=headers, auth=auth)
logs = response.json()

print(f"Total de logs: {logs['count']}")
for log in logs['results']:
    print(f"{log['timestamp']} - {log['username']} - {log['action_display']}")
```

---

### Consulta con Llave de Desarrollador

```python
import requests
import os

url = "http://localhost:8000/api/audit/developer-access/"
headers = {
    "X-Developer-Key": os.getenv('AUDIT_DEVELOPER_KEY')
}

response = requests.get(url, headers=headers)
data = response.json()

print(f"Acceso autorizado: {data['message']}")
print(f"Total de registros: {data['total_records']}")

for log in data['results']:
    print(f"{log['timestamp']} - {log['username']} - {log['action_display']} - IP: {log['ip_address']}")
```

---

### Filtrar Logs de Intentos Fallidos

```python
import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:8000/api/audit/"
params = {
    "action": "LOGIN_FAILED",
    "date_from": "2025-11-01"
}
headers = {
    "X-Organization-Subdomain": "mi-organizacion"
}
auth = HTTPBasicAuth('admin', 'password')

response = requests.get(url, params=params, headers=headers, auth=auth)
logs = response.json()

print(f"Intentos fallidos de login: {logs['count']}")
for log in logs['results']:
    print(f"⚠️  {log['timestamp']} - {log['username']} - IP: {log['ip_address']}")
    print(f"   Descripción: {log['description']}")
```

---

## 🔒 Mejores Prácticas de Seguridad

1. **Nunca compartir la llave de desarrollador**
   - Mantenerla en `.env` (no en el código)
   - No subirla a repositorios Git
   - Rotarla periódicamente

2. **Usar HTTPS en producción**
   ```bash
   # ❌ NO usar en producción
   http://api.example.com/api/audit/
   
   # ✅ Usar en producción
   https://api.example.com/api/audit/
   ```

3. **Limitar acceso al endpoint de desarrollador**
   - Solo desde IPs específicas (firewall)
   - Solo en entornos de desarrollo/staging
   - Deshabilitar en producción si no es necesario

4. **Monitorear uso del endpoint de desarrollador**
   - Registrar cada acceso
   - Alertar sobre uso sospechoso
   - Auditar regularmente

---

## 📝 Notas Adicionales

- Los logs son **solo lectura** (no se pueden modificar ni eliminar vía API)
- La paginación por defecto es de 25 registros por página
- Los timestamps están en zona horaria `America/La_Paz` (Bolivia)
- El campo `user_agent` captura información del navegador/cliente
- Los logs se mantienen indefinidamente (considerar rotación periódica)

---

## 🧪 Probar el Sistema

Ejecutar el script de prueba:

```bash
cd Backend
python test_audit_system.py
```

Este script:
- ✅ Crea logs de ejemplo
- ✅ Prueba consultas y filtros
- ✅ Verifica la configuración de la llave de desarrollador
- ✅ Muestra ejemplos de uso
