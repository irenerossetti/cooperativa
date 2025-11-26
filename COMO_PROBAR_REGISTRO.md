# 🧪 Cómo Probar el Registro de Organizaciones

## 🚀 Paso 1: Iniciar el servidor

```bash
cd Backend
python manage.py runserver
```

El servidor debe estar corriendo en `http://localhost:8000`

## 🌐 Opción 1: Probar desde el navegador (MÁS FÁCIL)

1. Abre el archivo `test_register.html` en tu navegador:
   - Doble clic en el archivo, o
   - Arrastra el archivo al navegador

2. Completa el formulario con los datos de tu organización

3. Haz clic en "Registrar Organización"

4. ¡Listo! Verás el resultado inmediatamente

### Datos de ejemplo:

```
Organización:
- Nombre: Cooperativa Prueba
- Subdominio: prueba
- Email: contacto@prueba.com
- Teléfono: +591 3 1234567

Usuario:
- Username: adminprueba
- Email: admin@prueba.com
- Password: password123
- Nombre: Admin
- Apellido: Prueba
```

## 💻 Opción 2: Probar con Python

```bash
cd Backend
pip install requests  # Si no lo tienes instalado
python test_register_organization.py
```

## 🔧 Opción 3: Probar con curl

```bash
curl -X POST http://localhost:8000/api/tenants/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Mi Cooperativa",
    "subdomain": "micooperativa",
    "email": "contacto@micooperativa.com",
    "phone": "+591 3 1234567",
    "username": "admin",
    "user_email": "admin@micooperativa.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

## 🔍 Opción 4: Probar con Postman/Insomnia

1. **Método**: POST
2. **URL**: `http://localhost:8000/api/tenants/register/`
3. **Headers**: 
   - `Content-Type: application/json`
4. **Body** (raw JSON):
```json
{
    "organization_name": "Mi Cooperativa",
    "subdomain": "micooperativa",
    "email": "contacto@micooperativa.com",
    "phone": "+591 3 1234567",
    "username": "admin",
    "user_email": "admin@micooperativa.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez"
}
```

## ✅ Respuesta exitosa

```json
{
    "message": "Organización registrada exitosamente",
    "organization": {
        "id": 4,
        "name": "Mi Cooperativa",
        "subdomain": "micooperativa",
        "plan": "FREE",
        "status": "TRIAL"
    },
    "user": {
        "id": 18,
        "username": "admin",
        "email": "admin@micooperativa.com"
    }
}
```

## ❌ Errores comunes

### Error: "Este subdominio ya está en uso"
**Solución**: Usa un subdominio diferente

### Error: "Este nombre de usuario ya está en uso"
**Solución**: Usa un username diferente

### Error: "No se pudo conectar al servidor"
**Solución**: Asegúrate de que el servidor esté corriendo:
```bash
python manage.py runserver
```

### Error: "Organización no encontrada"
**Solución**: Este error no debería aparecer en el registro. Si aparece, verifica que el middleware esté configurado correctamente.

## 🧪 Verificar que funcionó

### 1. Ver en el admin de Django:
```
http://localhost:8000/admin/tenants/organization/
```

### 2. Listar organizaciones del usuario:
```bash
curl http://localhost:8000/api/tenants/my-organizations/ \
  -u admin:password123
```

### 3. Probar acceso con la organización:
```bash
# Método 1: Query parameter
curl http://localhost:8000/api/partners/?org=micooperativa

# Método 2: Header
curl -H "X-Organization-Subdomain: micooperativa" \
     http://localhost:8000/api/partners/
```

## 📊 Ver todas las organizaciones

```bash
python test_multi_tenant.py
```

Esto mostrará:
- Todas las organizaciones creadas
- Membresías
- Estadísticas
- Distribución de planes

## 🎯 Próximos pasos después de registrar

1. **Login con el usuario creado**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password123"}'
   ```

2. **Acceder a las APIs con tu organización**:
   - Agrega `?org=tusubdominio` a cualquier URL
   - O usa el header `X-Organization-Subdomain: tusubdominio`

3. **Crear datos en tu organización**:
   - Partners
   - Products
   - Orders
   - etc.

## 🔐 Seguridad

- Los datos de cada organización están completamente aislados
- No puedes ver datos de otras organizaciones
- Cada organización tiene su propio conjunto de usuarios y permisos

## 📞 Soporte

Si tienes problemas:
1. Verifica que el servidor esté corriendo
2. Revisa los logs del servidor
3. Verifica que el middleware esté configurado en `settings.py`
4. Consulta `MULTI_TENANT_GUIDE.md` para más detalles

## 🎉 ¡Listo!

Ahora puedes registrar organizaciones y empezar a usar el sistema multi-tenant.
