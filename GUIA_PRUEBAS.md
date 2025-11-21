# 🧪 Guía de Pruebas - CRUD Completo

## Método 1: Navegador (MÁS FÁCIL) 🌐

### Paso 1: Inicia el servidor
```bash
python manage.py runserver
```

### Paso 2: Abre estos enlaces en tu navegador

#### 🔐 Login primero
http://localhost:8000/api/auth/users/login/

**Datos:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

#### 👥 Probar CRUD de Socios
**Lista (GET ALL):**
http://localhost:8000/api/partners/partners/

**Crear (POST):** En la misma página, abajo hay un formulario
```json
{
  "ci": "7654321",
  "first_name": "María",
  "last_name": "González",
  "phone": "+59171234567",
  "community": 1,
  "status": "ACTIVE"
}
```

**Ver uno (GET BY ID):**
http://localhost:8000/api/partners/partners/1/

**Actualizar (PUT/PATCH):** En la página del detalle, hay botones para editar

**Eliminar (DELETE):** En la página del detalle, botón rojo "DELETE"

#### 🗺️ Probar CRUD de Parcelas
http://localhost:8000/api/parcels/parcels/

**Crear:**
```json
{
  "code": "P001",
  "name": "Parcela Norte",
  "surface": 5.5,
  "location": "Sector Norte",
  "partner": 1,
  "soil_type": 1,
  "current_crop": 1,
  "status": "ACTIVE"
}
```

#### 🏘️ Probar CRUD de Comunidades
http://localhost:8000/api/partners/communities/

#### 👤 Probar CRUD de Usuarios
http://localhost:8000/api/auth/users/

#### 📝 Ver Auditoría
http://localhost:8000/api/audit/logs/

---

## Método 2: Postman 📮

### Importar colección
1. Abre Postman
2. File → Import
3. Selecciona `Postman_Collection.json`
4. Ejecuta los requests en orden

### Orden de prueba:
1. **Login** - Guarda las cookies automáticamente
2. **GET Lista de Socios** - Ver todos
3. **POST Crear Socio** - Crear uno nuevo
4. **GET Socio por ID** - Ver el que creaste
5. **PATCH Actualizar Socio** - Modificar algo
6. **DELETE Eliminar Socio** - Eliminarlo

---

## Método 3: cURL (Terminal) 💻

### 1. Login y guardar cookies
```bash
curl -X POST http://localhost:8000/api/auth/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' \
  -c cookies.txt
```

### 2. GET - Listar todos los socios
```bash
curl -X GET http://localhost:8000/api/partners/partners/ \
  -b cookies.txt
```

### 3. POST - Crear un socio
```bash
curl -X POST http://localhost:8000/api/partners/partners/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "ci": "8765432",
    "first_name": "Pedro",
    "last_name": "López",
    "phone": "+59172345678",
    "community": 1,
    "status": "ACTIVE"
  }'
```

### 4. GET - Ver un socio específico
```bash
curl -X GET http://localhost:8000/api/partners/partners/1/ \
  -b cookies.txt
```

### 5. PATCH - Actualizar un socio
```bash
curl -X PATCH http://localhost:8000/api/partners/partners/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"phone": "+59179999999"}'
```

### 6. DELETE - Eliminar un socio
```bash
curl -X DELETE http://localhost:8000/api/partners/partners/1/ \
  -b cookies.txt
```

---

## Método 4: Python Script 🐍

Ya tienes `test_api.py` que prueba todo automáticamente:

```bash
python test_api.py
```

---

## Checklist de Pruebas ✅

### Socios (Partners)
- [ ] GET /api/partners/partners/ - Listar todos
- [ ] GET /api/partners/partners/1/ - Ver uno
- [ ] POST /api/partners/partners/ - Crear
- [ ] PUT /api/partners/partners/1/ - Actualizar completo
- [ ] PATCH /api/partners/partners/1/ - Actualizar parcial
- [ ] DELETE /api/partners/partners/1/ - Eliminar
- [ ] POST /api/partners/partners/1/deactivate/ - Inhabilitar
- [ ] POST /api/partners/partners/1/activate/ - Reactivar

### Parcelas (Parcels)
- [ ] GET /api/parcels/parcels/ - Listar todas
- [ ] GET /api/parcels/parcels/1/ - Ver una
- [ ] POST /api/parcels/parcels/ - Crear
- [ ] PATCH /api/parcels/parcels/1/ - Actualizar
- [ ] DELETE /api/parcels/parcels/1/ - Eliminar

### Usuarios (Users)
- [ ] GET /api/auth/users/ - Listar todos
- [ ] GET /api/auth/users/1/ - Ver uno
- [ ] POST /api/auth/users/ - Crear
- [ ] PATCH /api/auth/users/1/ - Actualizar
- [ ] DELETE /api/auth/users/1/ - Eliminar

### Comunidades (Communities)
- [ ] GET /api/partners/communities/ - Listar todas
- [ ] GET /api/partners/communities/1/ - Ver una
- [ ] POST /api/partners/communities/ - Crear
- [ ] PATCH /api/partners/communities/1/ - Actualizar

### Filtros y Búsquedas
- [ ] GET /api/partners/partners/?search=juan
- [ ] GET /api/partners/partners/?community=1
- [ ] GET /api/partners/partners/?status=ACTIVE
- [ ] GET /api/parcels/parcels/?partner=1
- [ ] GET /api/audit/logs/?action=LOGIN

---

## Validaciones a Probar 🔍

### Socios
1. **CI duplicado** - Intenta crear dos socios con el mismo CI
   - ❌ Debe fallar con error
2. **NIT duplicado** - Intenta crear dos socios con el mismo NIT
   - ❌ Debe fallar con error
3. **Email inválido** - Intenta crear con email sin @
   - ❌ Debe fallar con error
4. **Teléfono inválido** - Intenta crear con teléfono corto
   - ❌ Debe fallar con error

### Parcelas
1. **Código duplicado** - Intenta crear dos parcelas con el mismo código
   - ❌ Debe fallar con error
2. **Superficie negativa** - Intenta crear con surface = -5
   - ❌ Debe fallar con error
3. **Superficie cero** - Intenta crear con surface = 0
   - ❌ Debe fallar con error

### Usuarios
1. **Username duplicado** - Intenta crear dos usuarios con el mismo username
   - ❌ Debe fallar con error
2. **Email duplicado** - Intenta crear dos usuarios con el mismo email
   - ❌ Debe fallar con error

---

## Resultados Esperados 📊

### GET (Listar)
- Status: 200 OK
- Response: Lista paginada con count, next, previous, results

### GET (Detalle)
- Status: 200 OK
- Response: Objeto completo con todos los campos

### POST (Crear)
- Status: 201 Created
- Response: Objeto creado con ID asignado

### PUT/PATCH (Actualizar)
- Status: 200 OK
- Response: Objeto actualizado

### DELETE (Eliminar)
- Status: 204 No Content
- Response: Sin contenido

### Errores
- 400 Bad Request - Datos inválidos
- 401 Unauthorized - No autenticado
- 403 Forbidden - Sin permisos
- 404 Not Found - No existe
- 500 Internal Server Error - Error del servidor

---

## 🎯 Recomendación

**Para pruebas rápidas:** Usa el navegador (Método 1)
**Para pruebas completas:** Usa Postman (Método 2)
**Para automatización:** Usa el script Python (Método 4)
