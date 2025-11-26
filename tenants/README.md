# 🏢 Tenants - Sistema Multi-Tenant

Sistema de multi-tenancy para permitir que múltiples cooperativas usen la misma aplicación con datos completamente aislados.

## 🎯 Propósito

Convertir el sistema cooperativo en un **SaaS (Software as a Service)** donde cada cooperativa es un "tenant" independiente con:
- Datos completamente aislados
- Subdominios personalizados
- Planes de suscripción
- Gestión de usuarios por organización

## 📦 Componentes

### Modelos

#### Organization
Representa una cooperativa (tenant).

**Campos principales:**
- `name`: Nombre de la cooperativa
- `subdomain`: Subdominio único (ej: `cooperativa1`)
- `plan`: Plan de suscripción (FREE, BASIC, PROFESSIONAL, ENTERPRISE)
- `status`: Estado (TRIAL, ACTIVE, SUSPENDED, CANCELLED)
- `max_users`, `max_products`, `max_storage_mb`: Límites según el plan

#### OrganizationMember
Relación entre usuarios y organizaciones.

**Roles:**
- `OWNER`: Propietario (control total)
- `ADMIN`: Administrador (gestión de usuarios)
- `MEMBER`: Miembro (acceso según permisos)

### Middleware

**TenantMiddleware**: Detecta automáticamente la organización actual mediante:
1. Subdominio (ej: `cooperativa1.tuapp.com`)
2. Header HTTP (`X-Organization-Subdomain: cooperativa1`)
3. Query parameter (`?org=cooperativa1`)

### Managers

**TenantManager**: Filtra automáticamente todas las queries por la organización actual.

**TenantModel**: Clase base abstracta para modelos multi-tenant. Agrega:
- Campo `organization` (ForeignKey)
- Manager con filtrado automático
- Auto-asignación de organización al guardar

## 🚀 Uso

### Crear un modelo multi-tenant

```python
from tenants.managers import TenantModel

class Product(TenantModel):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # El campo 'organization' se agrega automáticamente
```

### Obtener la organización actual

```python
from tenants.middleware import get_current_organization

def my_view(request):
    org = get_current_organization()
    # o también:
    org = request.organization
```

### Queries automáticas

```python
# Automáticamente filtra por la organización actual
products = Product.objects.all()

# Para obtener de todas las organizaciones (solo admin)
all_products = Product.objects.all_organizations()
```

## 🔌 API

### Registrar nueva organización (público)

```http
POST /api/tenants/register/
Content-Type: application/json

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

### Listar mis organizaciones

```http
GET /api/tenants/my-organizations/
Authorization: Session/Token
```

### Obtener organización actual

```http
GET /api/tenants/organizations/current/
X-Organization-Subdomain: cooperativa1
```

## 🧪 Testing

### Crear datos de prueba

```bash
python create_test_organizations.py
```

Esto crea:
- 3 organizaciones (sanjuan, progreso, demo)
- 3 usuarios (admin, socio1, cliente1)
- 5 membresías

### Probar con curl

```bash
# Método 1: Query parameter
curl http://localhost:8000/api/products/?org=sanjuan

# Método 2: Header HTTP
curl -H "X-Organization-Subdomain: sanjuan" \
     http://localhost:8000/api/products/

# Método 3: Subdominio (requiere DNS)
curl http://sanjuan.localhost:8000/api/products/
```

## 📊 Planes

| Plan | Usuarios | Productos | Almacenamiento | Precio |
|------|----------|-----------|----------------|--------|
| FREE | 5 | 100 | 100 MB | Gratis |
| BASIC | 10 | 500 | 500 MB | $29/mes |
| PROFESSIONAL | 20 | 1000 | 1 GB | $79/mes |
| ENTERPRISE | Ilimitado | Ilimitado | 10 GB | $199/mes |

## 🔐 Seguridad

- ✅ Datos completamente aislados por organización
- ✅ Queries filtradas automáticamente
- ✅ No es posible acceder a datos de otra organización
- ✅ Validación de permisos por rol

## 📚 Documentación

- **Guía completa**: `../MULTI_TENANT_GUIDE.md`
- **Ejemplo de migración**: `../EJEMPLO_MIGRACION_TENANT.md`
- **Resumen ejecutivo**: `../SAAS_IMPLEMENTATION_SUMMARY.md`
- **Lista de archivos**: `../ARCHIVOS_MULTI_TENANT.md`

## 🔄 Migración de modelos existentes

Ver `../EJEMPLO_MIGRACION_TENANT.md` para instrucciones detalladas.

Pasos básicos:
1. Cambiar `models.Model` por `TenantModel`
2. Crear migración
3. Asignar organización a datos existentes
4. Aplicar migración

## 🎯 Próximos pasos

- [ ] Migrar todos los modelos a multi-tenant
- [ ] Implementar sistema de suscripciones
- [ ] Integrar pasarela de pagos
- [ ] Crear landing page pública
- [ ] Dashboard de administración

## 📞 Soporte

Para dudas o problemas, consulta la documentación completa en los archivos mencionados arriba.
