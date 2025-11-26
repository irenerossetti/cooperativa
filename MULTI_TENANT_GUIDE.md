# Guía de Multi-Tenancy (SaaS)

## 📋 Descripción

El sistema ahora soporta **multi-tenancy**, permitiendo que múltiples cooperativas (organizaciones) usen la misma instancia de la aplicación con datos completamente aislados.

## 🏗️ Arquitectura

### Componentes principales:

1. **Organization (Tenant)**: Representa una cooperativa
2. **OrganizationMember**: Relación entre usuarios y organizaciones
3. **TenantMiddleware**: Detecta y establece la organización actual
4. **TenantManager**: Filtra automáticamente queries por organización

## 🚀 Cómo funciona

### Detección de Tenant

El middleware detecta la organización actual mediante 3 métodos (en orden de prioridad):

1. **Subdominio**: `cooperativa1.tuapp.com`
2. **Header HTTP**: `X-Organization-Subdomain: cooperativa1`
3. **Query Parameter**: `?org=cooperativa1`

### Aislamiento de datos

Todos los modelos que hereden de `TenantModel` automáticamente:
- Tienen un campo `organization`
- Se filtran por la organización actual
- Se auto-asignan a la organización en el contexto

## 📦 Modelos

### Organization

```python
{
    "id": 1,
    "name": "Cooperativa San Juan",
    "subdomain": "sanjuan",
    "email": "contacto@sanjuan.coop",
    "plan": "PROFESSIONAL",  # FREE, BASIC, PROFESSIONAL, ENTERPRISE
    "status": "ACTIVE",      # TRIAL, ACTIVE, SUSPENDED, CANCELLED
    "max_users": 20,
    "max_products": 1000,
    "max_storage_mb": 1000,
    "is_active": true
}
```

### OrganizationMember

```python
{
    "id": 1,
    "organization": 1,
    "user": 1,
    "role": "OWNER",  # OWNER, ADMIN, MEMBER
    "is_active": true
}
```

## 🔌 API Endpoints

### Registro de Organización (Público)

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
X-Organization-Subdomain: sanjuan
```

### Listar miembros de una organización

```http
GET /api/tenants/organizations/{id}/members/
X-Organization-Subdomain: sanjuan
```

## 💻 Uso en el código

### Convertir un modelo existente a multi-tenant

**Antes:**
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

**Después:**
```python
from tenants.managers import TenantModel

class Product(TenantModel):  # Hereda de TenantModel
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # El campo 'organization' se agrega automáticamente
```

### Queries automáticas

```python
# Automáticamente filtra por la organización actual
products = Product.objects.all()

# Para obtener de todas las organizaciones (admin)
all_products = Product.objects.all_organizations()
```

### Obtener organización actual

```python
from tenants.middleware import get_current_organization

def my_view(request):
    org = get_current_organization()
    # o también:
    org = request.organization
```

## 🧪 Testing

### Desarrollo local

Puedes usar cualquiera de estos métodos:

**1. Query Parameter (más fácil para desarrollo):**
```
http://localhost:8000/api/products/?org=sanjuan
```

**2. Header HTTP:**
```bash
curl -H "X-Organization-Subdomain: sanjuan" \
     http://localhost:8000/api/products/
```

**3. Subdominio (requiere configuración DNS local):**
```
http://sanjuan.localhost:8000/api/products/
```

### Organizaciones de prueba

Ejecuta el script para crear organizaciones de prueba:

```bash
python create_test_organizations.py
```

Organizaciones creadas:
- **sanjuan** - Cooperativa San Juan (PROFESSIONAL)
- **progreso** - Cooperativa El Progreso (BASIC)
- **demo** - Cooperativa Demo (FREE/TRIAL)

Usuarios:
- **admin** / admin123 (Owner de todas)
- **socio1** / socio123 (Admin de San Juan)
- **cliente1** / cliente123 (Member de San Juan)

## 📊 Planes y Límites

### Planes disponibles

| Plan | Usuarios | Productos | Almacenamiento | Precio |
|------|----------|-----------|----------------|--------|
| FREE | 5 | 100 | 100 MB | Gratis |
| BASIC | 10 | 500 | 500 MB | $29/mes |
| PROFESSIONAL | 20 | 1000 | 1 GB | $79/mes |
| ENTERPRISE | Ilimitado | Ilimitado | 10 GB | $199/mes |

### Validar límites

```python
from tenants.middleware import get_current_organization

def create_user(request):
    org = get_current_organization()
    
    # Verificar límite de usuarios
    current_users = org.members.filter(is_active=True).count()
    if current_users >= org.max_users:
        return Response({
            'error': 'Límite de usuarios alcanzado',
            'current': current_users,
            'max': org.max_users,
            'plan': org.plan
        }, status=400)
    
    # Crear usuario...
```

## 🔐 Seguridad

### Aislamiento de datos

- Cada organización solo ve sus propios datos
- Los filtros se aplican automáticamente en el ORM
- No es posible acceder a datos de otra organización

### Roles de organización

- **OWNER**: Control total, puede eliminar la organización
- **ADMIN**: Puede gestionar usuarios y configuración
- **MEMBER**: Acceso según permisos del sistema

## 🚀 Próximos pasos

### Para convertir el sistema completo a multi-tenant:

1. **Migrar modelos existentes** (uno por uno):
   ```python
   # Agregar campo organization a cada modelo
   organization = models.ForeignKey('tenants.Organization', on_delete=models.CASCADE)
   ```

2. **Crear migraciones**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Asignar organizaciones a datos existentes**:
   ```python
   # Script para asignar organización por defecto
   default_org = Organization.objects.first()
   Model.objects.update(organization=default_org)
   ```

4. **Actualizar vistas y serializers** para usar el contexto de organización

5. **Implementar sistema de suscripciones** (Stripe/PayPal)

6. **Crear landing page** para registro público

## 📝 Notas importantes

- El middleware debe estar después de `AuthenticationMiddleware`
- Las rutas públicas (login, registro) no requieren organización
- Los datos existentes necesitan ser migrados a una organización
- Considera usar PostgreSQL para producción (mejor rendimiento con índices)

## 🆘 Troubleshooting

### Error: "Organización no encontrada"

- Verifica que estés enviando el subdominio/header/query correcto
- Verifica que la organización existe y está activa
- Verifica que la ruta no esté en la lista de rutas públicas

### Error: "No se puede guardar sin una organización"

- Asegúrate de que el middleware esté configurado
- Verifica que estés en un contexto con organización
- Para operaciones admin, asigna manualmente la organización

### Los datos no se filtran correctamente

- Verifica que el modelo herede de `TenantModel`
- Verifica que uses `objects` (no `_base_manager`)
- Verifica que el middleware esté activo

## 📚 Referencias

- [Django Multi-Tenancy Patterns](https://books.agiliq.com/projects/django-multi-tenant/en/latest/)
- [SaaS Best Practices](https://www.saas-metrics.co/)
