# Solución al Error 403 - Forbidden

## Problema Identificado

El error 403 en todos los endpoints se debe a que:

1. **El backend NO tenía JWT configurado** - Estaba usando solo SessionAuthentication y BasicAuthentication
2. **El frontend envía tokens JWT** - Pero el backend no los reconocía
3. **Resultado**: Todas las peticiones autenticadas fallaban con 403

## Archivos Modificados

### 1. `requirements.txt`
✅ Agregado: `djangorestframework-simplejwt>=5.3.0`

### 2. `config/settings.py`
✅ Actualizado REST_FRAMEWORK para incluir JWTAuthentication
✅ Agregada configuración SIMPLE_JWT

### 3. `config/urls.py`
✅ Agregados endpoints JWT:
- `/api/token/` - Obtener tokens
- `/api/token/refresh/` - Refrescar token

### 4. `users/views.py`
✅ Actualizado endpoint de login para devolver tokens JWT

## Pasos para Aplicar la Solución

### En el servidor (Render o local):

```bash
# 1. Instalar la dependencia JWT
pip install djangorestframework-simplejwt

# 2. Vincular usuarios a organizaciones (si es necesario)
python fix_authentication.py

# 3. Reiniciar el servidor
# En Render: Se reiniciará automáticamente al hacer push
# En local: Ctrl+C y volver a ejecutar python manage.py runserver
```

### Verificar que funciona:

```bash
# Test 1: Obtener token
curl -X POST https://cooperativa-epws.onrender.com/api/auth/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Deberías recibir:
# {
#   "message": "Inicio de sesión exitoso",
#   "user": {...},
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }

# Test 2: Usar el token para acceder a un endpoint protegido
curl -X GET https://cooperativa-epws.onrender.com/api/partners/partners/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "X-Organization-Subdomain: sanjuan"
```

## Qué Cambió

### Antes:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # ❌ Solo sesiones
        'rest_framework.authentication.BasicAuthentication',     # ❌ Solo basic auth
    ],
}
```

### Ahora:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # ✅ JWT primero
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}
```

### Login Response Antes:
```json
{
  "message": "Inicio de sesión exitoso",
  "user": {...}
}
```

### Login Response Ahora:
```json
{
  "message": "Inicio de sesión exitoso",
  "user": {...},
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",  // ✅ Token de acceso
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."  // ✅ Token de refresco
}
```

## Frontend

El frontend ya está configurado correctamente para usar JWT. Una vez que el backend esté actualizado:

1. El usuario hace login
2. Recibe los tokens `access` y `refresh`
3. El frontend guarda los tokens en localStorage
4. Todas las peticiones incluyen: `Authorization: Bearer {access_token}`
5. El backend ahora reconoce y valida estos tokens ✅

## Deployment en Render

1. Hacer commit de los cambios:
```bash
git add .
git commit -m "Fix: Agregar autenticación JWT para solucionar error 403"
git push
```

2. Render detectará los cambios en `requirements.txt`
3. Instalará `djangorestframework-simplejwt` automáticamente
4. Reiniciará el servidor con la nueva configuración

## Verificación Post-Deploy

Una vez desplegado, verifica:

1. ✅ Login devuelve tokens JWT
2. ✅ Endpoints protegidos aceptan `Authorization: Bearer {token}`
3. ✅ No más errores 403 en el frontend
4. ✅ Dashboard carga correctamente

## Notas Importantes

- Los tokens de acceso duran **1 día**
- Los tokens de refresco duran **7 días**
- El frontend debe refrescar el token antes de que expire
- Los usuarios existentes deben volver a hacer login para obtener tokens JWT

## Troubleshooting

### Si siguen los errores 403:

1. Verificar que el token se está enviando correctamente:
```javascript
// En el frontend, verificar que axios incluye:
headers: {
  'Authorization': `Bearer ${token}`
}
```

2. Verificar que el usuario tiene partner asociado:
```bash
python fix_authentication.py
```

3. Verificar logs del servidor para ver el error exacto

### Si el login no devuelve tokens:

1. Verificar que djangorestframework-simplejwt está instalado:
```bash
pip list | grep simplejwt
```

2. Verificar que settings.py tiene la configuración SIMPLE_JWT

3. Reiniciar el servidor completamente
