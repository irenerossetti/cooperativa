# 📁 Archivos del Sistema Multi-Tenant

## Archivos creados

### App `tenants/`

```
Backend/tenants/
├── __init__.py                 # Configuración de la app
├── apps.py                     # Configuración de Django app
├── models.py                   # Modelos Organization y OrganizationMember
├── admin.py                    # Admin de Django para gestión
├── managers.py                 # TenantManager y TenantModel
├── middleware.py               # TenantMiddleware para detección
├── serializers.py              # Serializers de DRF
├── views.py                    # ViewSets y endpoints
├── urls.py                     # Rutas de la API
└── migrations/
    └── 0001_initial.py         # Migración inicial
```

### Scripts de utilidad

```
Backend/
├── create_test_organizations.py    # Crear organizaciones de prueba
├── test_multi_tenant.py            # Verificar funcionamiento
└── migrate_partners_to_tenant.py   # (Ejemplo en documentación)
```

### Documentación

```
Backend/
├── SAAS_IMPLEMENTATION_SUMMARY.md  # Resumen ejecutivo
├── MULTI_TENANT_GUIDE.md           # Guía completa del sistema
├── EJEMPLO_MIGRACION_TENANT.md     # Cómo migrar modelos
└── ARCHIVOS_MULTI_TENANT.md        # Este archivo
```

### Archivos modificados

```
Backend/config/
├── settings.py                 # Agregado 'tenants' a INSTALLED_APPS
│                              # Agregado TenantMiddleware a MIDDLEWARE
└── urls.py                    # Agregado path('api/tenants/', ...)
```

## Estructura de la base de datos

### Nuevas tablas

```sql
-- Tabla de organizaciones
CREATE TABLE tenants_organization (
    id BIGINT PRIMARY KEY,
    name VARCHAR(200),
    slug VARCHAR(200) UNIQUE,
    subdomain VARCHAR(63) UNIQUE,
    email VARCHAR(254),
    phone VARCHAR(20),
    address TEXT,
    plan VARCHAR(20),
    status VARCHAR(20),
    max_users INTEGER,
    max_products INTEGER,
    max_storage_mb INTEGER,
    is_active BOOLEAN,
    settings JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    trial_ends_at TIMESTAMP,
    subscription_ends_at TIMESTAMP
);

-- Tabla de membresías
CREATE TABLE tenants_organization_member (
    id BIGINT PRIMARY KEY,
    organization_id BIGINT REFERENCES tenants_organization(id),
    user_id BIGINT REFERENCES users_user(id),
    role VARCHAR(20),
    is_active BOOLEAN,
    joined_at TIMESTAMP,
    UNIQUE(organization_id, user_id)
);
```

## API Endpoints

### Públicos (sin autenticación)

```
POST   /api/tenants/register/              # Registrar nueva organización
```

### Autenticados

```
GET    /api/tenants/my-organizations/      # Mis organizaciones
GET    /api/tenants/organizations/         # Listar organizaciones
POST   /api/tenants/organizations/         # Crear organización
GET    /api/tenants/organizations/{id}/    # Detalle de organización
PUT    /api/tenants/organizations/{id}/    # Actualizar organización
DELETE /api/tenants/organizations/{id}/    # Eliminar organización
GET    /api/tenants/organizations/current/ # Organización actual
GET    /api/tenants/organizations/{id}/members/     # Miembros
POST   /api/tenants/organizations/{id}/add_member/  # Agregar miembro
```

## Configuración requerida

### settings.py

```python
INSTALLED_APPS = [
    # ...
    'tenants',  # ← Agregado
    # ...
]

MIDDLEWARE = [
    # ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'tenants.middleware.TenantMiddleware',  # ← Agregado (después de Auth)
    # ...
]
```

### urls.py

```python
urlpatterns = [
    # ...
    path('api/tenants/', include('tenants.urls')),  # ← Agregado
    # ...
]
```

## Uso en el código

### Importaciones comunes

```python
# Para modelos multi-tenant
from tenants.managers import TenantModel

# Para obtener organización actual
from tenants.middleware import get_current_organization

# Para modelos de tenants
from tenants.models import Organization, OrganizationMember
```

### Ejemplo de modelo multi-tenant

```python
from tenants.managers import TenantModel

class MiModelo(TenantModel):
    nombre = models.CharField(max_length=200)
    # El campo 'organization' se agrega automáticamente
```

### Ejemplo de vista

```python
from tenants.middleware import get_current_organization

def mi_vista(request):
    org = get_current_organization()
    # o también:
    org = request.organization
```

## Comandos útiles

### Crear organizaciones de prueba

```bash
python create_test_organizations.py
```

### Verificar sistema

```bash
python test_multi_tenant.py
```

### Crear migraciones

```bash
python manage.py makemigrations tenants
python manage.py migrate tenants
```

### Acceder al admin

```
http://localhost:8000/admin/tenants/organization/
http://localhost:8000/admin/tenants/organizationmember/
```

## Variables de entorno

No se requieren nuevas variables de entorno para el sistema básico.

Para producción con subdominios reales, configurar:

```env
# .env
ALLOWED_HOSTS=.tuapp.com,localhost,127.0.0.1
```

## Dependencias

No se requieren nuevas dependencias. El sistema usa:
- Django (ya instalado)
- Django REST Framework (ya instalado)

## Testing

### Datos de prueba

Después de ejecutar `create_test_organizations.py`:

**Organizaciones:**
- sanjuan (PROFESSIONAL)
- progreso (BASIC)
- demo (FREE/TRIAL)

**Usuarios:**
- admin / admin123 (Owner de todas)
- socio1 / socio123 (Admin de San Juan)
- cliente1 / cliente123 (Member de San Juan)

### Probar con curl

```bash
# Registrar nueva organización
curl -X POST http://localhost:8000/api/tenants/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Nueva Cooperativa",
    "subdomain": "nueva",
    "email": "contacto@nueva.com",
    "username": "admin",
    "user_email": "admin@nueva.com",
    "password": "password123",
    "first_name": "Admin",
    "last_name": "Usuario"
  }'

# Listar mis organizaciones
curl http://localhost:8000/api/tenants/my-organizations/ \
  -u admin:admin123

# Acceder con organización específica
curl http://localhost:8000/api/partners/?org=sanjuan
```

## Próximos pasos

1. **Migrar modelos existentes** siguiendo `EJEMPLO_MIGRACION_TENANT.md`
2. **Implementar límites** de plan (validar max_users, max_products)
3. **Integrar pagos** (Stripe/PayPal)
4. **Crear landing page** de registro público
5. **Dashboard de admin** para gestionar organizaciones

## Soporte

- **Guía completa**: `MULTI_TENANT_GUIDE.md`
- **Ejemplo de migración**: `EJEMPLO_MIGRACION_TENANT.md`
- **Resumen ejecutivo**: `SAAS_IMPLEMENTATION_SUMMARY.md`

## Changelog

### v1.0 (Noviembre 2025)
- ✅ Implementación inicial de multi-tenancy
- ✅ Modelos Organization y OrganizationMember
- ✅ Middleware de detección de tenant
- ✅ Manager para filtrado automático
- ✅ API completa de gestión
- ✅ Documentación completa
- ✅ Scripts de prueba
