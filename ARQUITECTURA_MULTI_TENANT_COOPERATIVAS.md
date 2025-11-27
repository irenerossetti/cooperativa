# 🏗️ ARQUITECTURA MULTI-TENANT - SISTEMA DE COOPERATIVAS AGRÍCOLAS

**Sistema Django Multi-Tenant con PostgreSQL (Shared Database, Shared Schema)**  
**Versión:** 1.0  
**Última actualización:** Noviembre 2024

---

## 📋 TABLA DE CONTENIDOS

1. [¿Qué es Multi-Tenant?](#qué-es-multi-tenant)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Modelo de Datos](#modelo-de-datos)
4. [Flujo de Requests](#flujo-de-requests)
5. [Middleware de Tenant](#middleware-de-tenant)
6. [Modelos y Apps](#modelos-y-apps)
7. [Gestión de Organizaciones](#gestión-de-organizaciones)
8. [Ejemplos Prácticos](#ejemplos-prácticos)
9. [Troubleshooting](#troubleshooting)

---

## 🤔 ¿Qué es Multi-Tenant?

**Multi-Tenant** es una arquitectura donde **múltiples clientes (tenants)** comparten la **misma infraestructura de aplicación**, pero **sus datos están completamente aislados**.

### En nuestro caso:
- **Cada cooperativa es un TENANT independiente**
- **Cada cooperativa tiene sus datos aislados** mediante filtrado por `organization_id`
- **Datos 100% aislados**: La Cooperativa A no puede ver datos de la Cooperativa B
- **Código compartido**: Todas las cooperativas usan el mismo código Django
- **Base de datos compartida**: Una sola base de datos PostgreSQL (Neon)
- **Schema compartido**: Todas las tablas en el schema `public`

### Ventajas:
✅ **Escalabilidad**: Agregar nueva cooperativa = crear registro (segundos)  
✅ **Aislamiento**: Datos separados por `organization_id` (seguridad)  
✅ **Mantenimiento**: Un solo código para todas las cooperativas  
✅ **Costos**: Un solo servidor y base de datos para múltiples clientes  
✅ **Simplicidad**: No requiere schemas separados de PostgreSQL  

### Modelo Implementado:
**Shared Database, Shared Schema** - Todas las cooperativas comparten:
- ✅ La misma base de datos
- ✅ El mismo schema (`public`)
- ✅ Las mismas tablas
- ✅ Filtrado automático por `organization_id`

---

## 🏛️ ARQUITECTURA DEL SISTEMA

```
┌─────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE (NEON)                   │
│                         Schema: public                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                  TABLAS COMPARTIDAS                       │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │                                                           │ │
│  │  Tabla: tenants_organization                              │ │
│  │  ├─ id: 1                                                 │ │
│  │  ├─ name: "Cooperativa San Juan"                          │ │
│  │  ├─ subdomain: "sanjuan"                                  │ │
│  │  ├─ status: "ACTIVE"                                      │ │
│  │  └─ plan: "FREE"                                          │ │
│  │                                                           │ │
│  │  ├─ id: 2                                                 │ │
│  │  ├─ name: "Cooperativa Sypha"                             │ │
│  │  ├─ subdomain: "syphita"                                  │ │
│  │  ├─ status: "TRIAL"                                       │ │
│  │  └─ plan: "FREE"                                          │ │
│  │                                                           │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │                                                           │ │
│  │  Tabla: partners_partner (Socios)                         │ │
│  │  ├─ id: 1, organization_id: 1, name: "Juan Pérez"        │ │
│  │  ├─ id: 2, organization_id: 1, name: "María López"       │ │
│  │  ├─ id: 3, organization_id: 2, name: "Pedro García"      │ │
│  │  └─ ... (10 socios de org 1, 0 socios de org 2)          │ │
│  │                                                           │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │                                                           │ │
│  │  Tabla: parcels_parcel (Parcelas)                         │ │
│  │  ├─ id: 1, organization_id: 1, partner_id: 1             │ │
│  │  ├─ id: 2, organization_id: 1, partner_id: 1             │ │
│  │  ├─ id: 3, organization_id: 1, partner_id: 2             │ │
│  │  └─ ... (15 parcelas de org 1, 0 parcelas de org 2)      │ │
│  │                                                           │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │                                                           │ │
│  │  Tabla: production_harvestedproduct (Productos)           │ │
│  │  ├─ id: 1, organization_id: 1, partner_id: 1             │ │
│  │  ├─ id: 2, organization_id: 1, partner_id: 2             │ │
│  │  └─ ... (productos solo de org 1)                        │ │
│  │                                                           │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │                                                           │ │
│  │  Tabla: campaigns_campaign (Campañas)                     │ │
│  │  ├─ id: 1, organization_id: 1, name: "Campaña 2024"      │ │
│  │  └─ ... (campañas solo de org 1)                         │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🔑 CLAVE DEL AISLAMIENTO:                                      │
│  Todas las tablas tienen campo: organization_id                │
│  El middleware filtra automáticamente por organización actual  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 MODELO DE DATOS

### Tabla Principal: `tenants_organization`

```python
class Organization(models.Model):
    """Representa una cooperativa agrícola"""
    
    # Identificación
    name = models.CharField(max_length=255)           # "Cooperativa San Juan"
    subdomain = models.CharField(max_length=63)       # "sanjuan"
    email = models.EmailField()                       # contacto@sanjuan.com
    phone = models.CharField(max_length=20)           # +54 264 123 4567
    
    # Suscripción
    plan = models.CharField(max_length=20)            # FREE, BASIC, PROFESSIONAL
    status = models.CharField(max_length=20)          # ACTIVE, TRIAL, SUSPENDED
    
    # Límites
    max_users = models.IntegerField(default=10)
    max_products = models.IntegerField(default=100)
    max_storage_mb = models.IntegerField(default=1000)
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    trial_end_date = models.DateTimeField(null=True)
    
    # Estado
    is_active = models.BooleanField(default=True)
```

### Tablas con `organization_id`:

Todas estas tablas tienen el campo `organization` que referencia a `Organization`:

```python
# partners/models.py
class Partner(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    ci = models.CharField(max_length=20)
    # ... más campos

# parcels/models.py
class Parcel(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # ... más campos

# production/models.py
class HarvestedProduct(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    # ... más campos

# campaigns/models.py
class Campaign(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    # ... más campos
```

---

## 🚀 FLUJO DE REQUESTS

### 1️⃣ Request desde Frontend (con header)

```
┌─────────────┐
│   Cliente   │
│  (Browser)  │
└──────┬──────┘
       │
       │ GET http://localhost:8000/api/partners/
       │ Headers: {
       │   "X-Organization-Subdomain": "sanjuan"
       │ }
       │
       ▼
┌──────────────────────────────────────────────┐
│  TenantMiddleware (CUSTOM)                   │
├──────────────────────────────────────────────┤
│  1. Lee header: X-Organization-Subdomain     │
│  2. Busca: Organization.objects.get(         │
│            subdomain='sanjuan')              │
│  3. Guarda en thread_local:                  │
│     _thread_locals.organization = org        │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│         partners/views.py                    │
├──────────────────────────────────────────────┤
│  class PartnerViewSet(viewsets.ModelViewSet):│
│      queryset = Partner.objects.all()        │
│                                              │
│  El TenantManager filtra automáticamente:    │
│  Partner.objects.filter(organization=org)    │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│         PostgreSQL Query                     │
├──────────────────────────────────────────────┤
│  SELECT * FROM partners_partner              │
│  WHERE organization_id = 1;                  │
│                                              │
│  Resultado: Solo socios de "San Juan"        │
└──────────────────────────────────────────────┘
```
│  TenantMiddleware (CUSTOM)                   │
├──────────────────────────────────────────────┤
│  1. Lee header: X-Organization-Subdomain     │
│  2. Busca: Organization.objects.get(         │
│            subdomain='sanjuan')              │
│  3. Guarda en thread_local:                  │
│     _thread_locals.organization = org        │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│         partners/views.py                    │
├──────────────────────────────────────────────┤
│  class PartnerViewSet(viewsets.ModelViewSet):│
│      queryset = Partner.objects.all()        │
│                                              │
│  El TenantManager filtra automáticamente:    │
│  Partner.objects.filter(organization=org)    │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│         PostgreSQL Query                     │
├──────────────────────────────────────────────┤
│  SELECT * FROM partners_partner              │
│  WHERE organization_id = 1;                  │
│                                              │
│  Resultado: Solo socios de "San Juan"        │
└──────────────────────────────────────────────┘
```

---

Continúa en el siguiente paso...


## ⚙️ MIDDLEWARE DE TENANT (PASO 2)

### Componentes del Sistema Multi-Tenant

El sistema multi-tenant se compone de 3 componentes principales:

1. **TenantMiddleware** - Detecta y establece la organización actual
2. **TenantManager** - Filtra automáticamente las queries por organización
3. **TenantModel** - Modelo base para todos los modelos con organización

---

### 1️⃣ TenantMiddleware

**Ubicación:** `Backend/tenants/middleware.py`

**Función:** Detecta la organización actual y la guarda en thread-local storage.

#### Métodos de Detección (en orden de prioridad):

```python
# Método 1: Por Subdominio
# URL: http://sanjuan.localhost:8000/api/partners/
# Detecta: "sanjuan" → Busca Organization(subdomain='sanjuan')

# Casos especiales de detección:
# - sanjuan.tuapp.com → 3 partes → detecta "sanjuan"
# - sanjuan.localhost → 2 partes → detecta "sanjuan" (si no es 'localhost' o '127')
# - localhost → 1 parte → NO detecta (requiere header o query param)
# - www.tuapp.com → ignora "www"
# - api.tuapp.com → ignora "api"
# - admin.tuapp.com → ignora "admin"

# Método 2: Por Header HTTP
# Header: X-Organization-Subdomain: sanjuan
# Útil para: APIs, desarrollo, aplicaciones móviles, testing

# Método 3: Por Query Parameter
# URL: http://localhost:8000/api/partners/?org=sanjuan
# Útil para: desarrollo, testing, debugging
```

#### Código del Middleware:

```python
class TenantMiddleware(MiddlewareMixin):
    """
    Middleware que detecta y establece el tenant actual
    """
    
    def process_request(self, request):
        # 1. Rutas públicas (NO requieren organización)
        public_paths = [
            '/api/auth/',                    # Login, registro
            '/api/register/',                # Registro público
            '/admin/',                       # Django admin
            '/api/tenants/register/',        # Registro de organizaciones
            '/api/tenants/my-organizations/', # Mis organizaciones
            '/api/tenants/super-admin/',     # Panel super admin
        ]
        
        is_public = any(request.path.startswith(path) for path in public_paths)
        
        if is_public:
            set_current_organization(None)
            request.organization = None
            return None
        
        # 2. Detectar organización
        organization = None
        
        # Método 1: Por subdominio
        host = request.get_host().split(':')[0]  # Remover puerto
        parts = host.split('.')
        
        # Si hay subdominio (ej: cooperativa1.localhost o cooperativa1.tuapp.com)
        if len(parts) > 2 or (len(parts) == 2 and parts[0] not in ['localhost', '127']):
            subdomain = parts[0]
            if subdomain not in ['www', 'api', 'admin']:
                try:
                    organization = Organization.objects.get(
                        subdomain=subdomain,
                        is_active=True
                    )
                except Organization.DoesNotExist:
                    pass
        
        # Método 2: Por header HTTP (útil para APIs y desarrollo)
        if not organization:
            subdomain = request.headers.get('X-Organization-Subdomain')
            if subdomain:
                try:
                    organization = Organization.objects.get(
                        subdomain=subdomain,
                        is_active=True
                    )
                except Organization.DoesNotExist:
                    pass
        
        # Método 3: Por query parameter (útil para desarrollo)
        if not organization:
            subdomain = request.GET.get('org')
            if subdomain:
                try:
                    organization = Organization.objects.get(
                        subdomain=subdomain,
                        is_active=True
                    )
                except Organization.DoesNotExist:
                    pass
        
        # 3. Establecer organización en thread-local
        set_current_organization(organization)
        request.organization = organization
        
        # 4. Validar que se encontró organización
        if not organization and request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'Organización no encontrada',
                'detail': 'Debe especificar una organización válida mediante subdominio, header X-Organization-Subdomain, o parámetro ?org='
            }, status=400)
        
        # 5. Validar acceso del usuario
        if organization and request.user.is_authenticated and not request.user.is_superuser:
            # No validar en /me/ para permitir que el usuario obtenga su info
            if '/users/me/' in request.path:
                return None
            
            # Usuarios ADMIN pueden acceder a todas las organizaciones
            is_admin = request.user.role and request.user.role.name == 'ADMIN'
            if is_admin:
                return None
            
            # Otros usuarios: verificar que tengan partner en esta org
            from partners.models import Partner
            has_access = Partner.objects.all_organizations().filter(
                organization=organization,
                user=request.user
            ).exists()
            
            if not has_access:
                return JsonResponse({
                    'error': 'Acceso denegado',
                    'detail': f'No tienes acceso a {organization.name}'
                }, status=403)
        
        return None
    
    def process_response(self, request, response):
        # Limpiar thread-local después de la request
        set_current_organization(None)
        return response
```

#### Thread-Local Storage:

```python
import threading

# Variable global thread-local
_thread_locals = threading.local()

def get_current_organization():
    """Obtiene la organización actual del thread"""
    return getattr(_thread_locals, 'organization', None)

def set_current_organization(organization):
    """Establece la organización actual en el thread"""
    _thread_locals.organization = organization
```

**¿Por qué thread-local?**
- Cada request HTTP se procesa en un thread separado
- Thread-local permite guardar datos específicos del thread
- La organización está disponible en cualquier parte del código
- Se limpia automáticamente al finalizar el request

---

### 2️⃣ TenantManager

**Ubicación:** `Backend/tenants/managers.py`

**Función:** Manager personalizado que filtra automáticamente todas las queries por la organización actual.

#### Código del Manager:

```python
class TenantManager(models.Manager):
    """
    Manager que filtra automáticamente por organización
    """
    
    def get_queryset(self):
        # Obtener queryset base
        queryset = super().get_queryset()
        
        # Obtener organización actual del thread-local
        organization = get_current_organization()
        
        # Si hay organización, filtrar por ella
        if organization:
            return queryset.filter(organization=organization)
        
        # Si no hay organización, retornar queryset sin filtrar
        return queryset
    
    def all_organizations(self):
        """
        Método especial para obtener datos de TODAS las organizaciones
        (sin filtro automático)
        """
        return super().get_queryset()
```

#### Uso del Manager:

```python
# En cualquier vista o función:

# Esto retorna SOLO los socios de la organización actual
partners = Partner.objects.all()

# Esto retorna socios de TODAS las organizaciones
all_partners = Partner.objects.all_organizations()

# Filtros adicionales se aplican sobre el filtro de organización
active_partners = Partner.objects.filter(status='ACTIVE')
# SQL: SELECT * FROM partners_partner WHERE organization_id = 1 AND status = 'ACTIVE'
```

---

### 3️⃣ TenantModel

**Ubicación:** `Backend/tenants/managers.py`

**Función:** Modelo base abstracto que todos los modelos multi-tenant deben heredar.

#### Código del Modelo Base:

```python
class TenantModel(models.Model):
    """
    Modelo base abstracto para modelos multi-tenant
    """
    
    # Campo de organización (obligatorio)
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Organización',
        db_index=True  # Índice para mejorar performance
    )
    
    # Manager personalizado
    objects = TenantManager()
    
    class Meta:
        abstract = True  # No crea tabla en la BD
    
    def save(self, *args, **kwargs):
        """
        Auto-asigna la organización actual si no está establecida
        """
        if not self.organization_id:
            organization = get_current_organization()
            
            if organization:
                self.organization = organization
            else:
                raise ValueError(
                    f'No se puede guardar {self.__class__.__name__} sin organización. '
                    'Asegúrate de que el middleware esté configurado.'
                )
        
        super().save(*args, **kwargs)
```

#### Uso del Modelo Base:

```python
# partners/models.py
from tenants.managers import TenantModel

class Partner(TenantModel):
    """
    Modelo de Socio - hereda de TenantModel
    """
    name = models.CharField(max_length=255)
    ci = models.CharField(max_length=20)
    # ... más campos
    
    # NO necesitas definir:
    # - organization (ya está en TenantModel)
    # - objects = TenantManager() (ya está en TenantModel)
```

---

### 🔄 Flujo Completo de una Request

```
┌─────────────────────────────────────────────────────────────┐
│  1. REQUEST LLEGA AL SERVIDOR                               │
├─────────────────────────────────────────────────────────────┤
│  GET /api/partners/                                         │
│  Header: X-Organization-Subdomain: sanjuan                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  2. TENANT MIDDLEWARE                                       │
├─────────────────────────────────────────────────────────────┤
│  • Lee header: X-Organization-Subdomain = "sanjuan"         │
│  • Busca: Organization.objects.get(subdomain='sanjuan')     │
│  • Encuentra: Organization(id=1, name="Cooperativa SJ")     │
│  • Guarda en thread-local: set_current_organization(org)    │
│  • Guarda en request: request.organization = org            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  3. VISTA (PartnerViewSet)                                  │
├─────────────────────────────────────────────────────────────┤
│  class PartnerViewSet(viewsets.ModelViewSet):               │
│      queryset = Partner.objects.all()                       │
│                                                             │
│  • Partner.objects usa TenantManager                        │
│  • TenantManager.get_queryset() se ejecuta                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  4. TENANT MANAGER                                          │
├─────────────────────────────────────────────────────────────┤
│  def get_queryset(self):                                    │
│      queryset = super().get_queryset()                      │
│      organization = get_current_organization()  # org id=1  │
│      return queryset.filter(organization=organization)      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  5. QUERY SQL                                               │
├─────────────────────────────────────────────────────────────┤
│  SELECT * FROM partners_partner                             │
│  WHERE organization_id = 1;                                 │
│                                                             │
│  Resultado: Solo socios de "Cooperativa San Juan"          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  6. RESPONSE                                                │
├─────────────────────────────────────────────────────────────┤
│  [                                                          │
│    {"id": 1, "name": "Juan Pérez", "organization": 1},     │
│    {"id": 2, "name": "María López", "organization": 1},    │
│    ...                                                      │
│  ]                                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  7. CLEANUP (process_response)                              │
├─────────────────────────────────────────────────────────────┤
│  • set_current_organization(None)                           │
│  • Limpia thread-local                                      │
└─────────────────────────────────────────────────────────────┘
```

---

### 🔐 Validación de Acceso

El middleware también valida que el usuario tenga acceso a la organización:

```python
# Casos de acceso:

# 1. Super Admin (is_superuser=True)
#    ✅ Acceso a TODAS las organizaciones

# 2. Usuario ADMIN (role.name='ADMIN')
#    ✅ Acceso a TODAS las organizaciones

# 3. Usuario SOCIO o CLIENTE
#    ✅ Solo acceso a organizaciones donde tiene Partner
#    ❌ Acceso denegado a otras organizaciones

# Ejemplo de validación:
if organization and request.user.is_authenticated:
    if request.user.is_superuser:
        return None  # Acceso permitido
    
    is_admin = request.user.role and request.user.role.name == 'ADMIN'
    if is_admin:
        return None  # Acceso permitido
    
    # Verificar partner
    has_access = Partner.objects.all_organizations().filter(
        organization=organization,
        user=request.user
    ).exists()
    
    if not has_access:
        return JsonResponse({'error': 'Acceso denegado'}, status=403)
```

---

### 📝 Configuración en settings.py

```python
# config/settings.py

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ⚠️ CORS debe ser PRIMERO
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'config.disable_csrf.DisableCSRFMiddleware',  # Deshabilitar CSRF para APIs
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # ⚠️ IMPORTANTE: TenantMiddleware debe estar DESPUÉS de AuthenticationMiddleware
    'tenants.middleware.TenantMiddleware',  # ← Multi-tenancy
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Orden Crítico de Middlewares:**

1. **CorsMiddleware** - PRIMERO para manejar CORS
2. **SecurityMiddleware** - Seguridad general
3. **SessionMiddleware** - Manejo de sesiones
4. **AuthenticationMiddleware** - Autenticación de usuarios
5. **TenantMiddleware** - Multi-tenancy (necesita `request.user`)
6. **MessagesMiddleware** - Mensajes flash
7. **ClickjackingMiddleware** - Protección XSS

**¿Por qué TenantMiddleware después de AuthenticationMiddleware?**
- Necesitamos `request.user` para validar acceso
- AuthenticationMiddleware establece `request.user`
- TenantMiddleware usa `request.user` para validar permisos

---

### 💡 Ejemplos Prácticos de Detección

#### Ejemplo 1: Detección por Subdominio (Producción)

```bash
# Request desde el frontend
curl https://sanjuan.tuapp.com/api/partners/

# El middleware detecta:
# - host = "sanjuan.tuapp.com"
# - parts = ["sanjuan", "tuapp", "com"]  # 3 partes
# - subdomain = "sanjuan"
# - Busca: Organization.objects.get(subdomain='sanjuan')
```

#### Ejemplo 2: Detección por Header (Desarrollo/API)

```bash
# Request con header HTTP
curl http://localhost:8000/api/partners/ \
  -H "X-Organization-Subdomain: sanjuan"

# El middleware detecta:
# - Método 1 (subdominio) falla: localhost no tiene subdominio
# - Método 2 (header) funciona: lee "sanjuan" del header
# - Busca: Organization.objects.get(subdomain='sanjuan')
```

#### Ejemplo 3: Detección por Query Parameter (Testing)

```bash
# Request con query parameter
curl http://localhost:8000/api/partners/?org=sanjuan

# El middleware detecta:
# - Método 1 (subdominio) falla
# - Método 2 (header) falla
# - Método 3 (query) funciona: lee "sanjuan" del parámetro
# - Busca: Organization.objects.get(subdomain='sanjuan')
```

#### Ejemplo 4: Localhost con Subdominio (Desarrollo)

```bash
# Request con subdominio en localhost
curl http://sanjuan.localhost:8000/api/partners/

# El middleware detecta:
# - host = "sanjuan.localhost"
# - parts = ["sanjuan", "localhost"]  # 2 partes
# - Condición: len(parts) == 2 and parts[0] not in ['localhost', '127']
# - subdomain = "sanjuan"
# - Busca: Organization.objects.get(subdomain='sanjuan')
```

---

### 🧪 Testing del Middleware

#### Test 1: Detección por Header

```python
# Test con header HTTP
response = client.get(
    '/api/partners/',
    HTTP_X_ORGANIZATION_SUBDOMAIN='sanjuan'
)

# Verifica que solo retorna socios de "sanjuan"
assert all(p['organization'] == 1 for p in response.json())
```

#### Test 2: Detección por Subdominio

```python
# Test con subdominio
response = client.get(
    '/api/partners/',
    HTTP_HOST='sanjuan.localhost:8000'
)

# Verifica que detecta la organización correcta
assert response.status_code == 200
```

#### Test 3: Sin Organización

```python
# Test sin organización
response = client.get('/api/partners/')

# Debe retornar error 400
assert response.status_code == 400
assert 'Organización no encontrada' in response.json()['error']
```

#### Test 4: Acceso Denegado

```python
# Usuario de org1 intenta acceder a org2
client.force_authenticate(user=user_org1)
response = client.get(
    '/api/partners/',
    HTTP_X_ORGANIZATION_SUBDOMAIN='org2'
)

# Debe retornar error 403
assert response.status_code == 403
assert 'Acceso denegado' in response.json()['error']
```

---

### ✅ Ventajas del Sistema

1. **Automático**: No necesitas filtrar manualmente en cada vista
2. **Seguro**: Imposible acceder a datos de otra organización por error
3. **Simple**: Solo heredar de `TenantModel` y listo
4. **Flexible**: 3 métodos de detección (subdominio, header, query)
5. **Performante**: Índice en `organization_id` para queries rápidas

---

### ⚠️ Consideraciones Importantes

1. **Rutas Públicas**: Deben estar en `public_paths` del middleware
2. **Super Admin**: Tiene acceso a todas las organizaciones
3. **Thread-Local**: Se limpia automáticamente después de cada request
4. **Índices**: El campo `organization` tiene índice para performance
5. **Cascada**: Si se elimina una organización, se eliminan todos sus datos

---

**Continúa en PASO 3: Modelos y Apps...**


## 📦 MODELOS Y APPS (PASO 3)

### Estructura de Apps del Proyecto

El sistema está organizado en las siguientes apps Django:

```
Backend/
├── tenants/          # Gestión de organizaciones (multi-tenant)
├── users/            # Usuarios y autenticación
├── partners/         # Socios y comunidades
├── parcels/          # Parcelas, cultivos, tipos de suelo
├── campaigns/        # Campañas agrícolas
├── production/       # Productos cosechados
├── farm_activities/  # Labores agrícolas
├── inventory/        # Inventario de insumos
├── sales/            # Ventas y pedidos
├── financial/        # Pagos y finanzas
├── reports/          # Reportes y análisis
├── audit/            # Auditoría y logs
├── weather/          # Clima y predicciones
├── chatbot/          # Chatbot con IA
├── alerts/           # Alertas y notificaciones
└── market_analysis/  # Análisis de mercado
```

---

### 1️⃣ App: `tenants` (Gestión de Organizaciones)

**Propósito:** Gestionar las cooperativas (organizaciones) del sistema.

#### Modelo: `Organization`

```python
class Organization(models.Model):
    """Representa una cooperativa agrícola"""
    
    # Identificación
    name = models.CharField(max_length=255)           # "Cooperativa San Juan"
    subdomain = models.CharField(max_length=63)       # "sanjuan"
    email = models.EmailField()                       # contacto@sanjuan.com
    phone = models.CharField(max_length=20)           # +54 264 123 4567
    
    # Suscripción
    PLAN_CHOICES = [
        ('FREE', 'Gratuito'),
        ('BASIC', 'Básico'),
        ('PROFESSIONAL', 'Profesional'),
        ('ENTERPRISE', 'Enterprise'),
    ]
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Activa'),
        ('TRIAL', 'Prueba'),
        ('SUSPENDED', 'Suspendida'),
        ('CANCELLED', 'Cancelada'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    # Límites
    max_users = models.IntegerField(default=10)
    max_products = models.IntegerField(default=100)
    max_storage_mb = models.IntegerField(default=1000)
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    trial_end_date = models.DateTimeField(null=True)
    
    # Estado
    is_active = models.BooleanField(default=True)
```

**Características:**
- ✅ NO hereda de `TenantModel` (es la tabla maestra)
- ✅ NO tiene campo `organization_id`
- ✅ Gestiona las cooperativas del sistema
- ✅ Define límites y planes de suscripción

---

### 2️⃣ App: `users` (Usuarios y Autenticación)

**Propósito:** Gestionar usuarios del sistema con roles y permisos.

#### Modelo: `User`

```python
class User(AbstractBaseUser, PermissionsMixin):
    """Usuario del sistema"""
    
    # Identificación
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    
    # Información personal
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    # Rol
    role = models.ForeignKey('Role', on_delete=models.PROTECT)
    
    # Estado
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Fechas
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
```

#### Modelo: `Role`

```python
class Role(models.Model):
    """Roles de usuario"""
    
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('SOCIO', 'Socio'),
        ('CLIENTE', 'Cliente'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES)
    description = models.TextField()
    permissions = models.ManyToManyField('Permission')
```

**Características:**
- ✅ NO hereda de `TenantModel` (usuarios son globales)
- ✅ Un usuario puede tener acceso a múltiples organizaciones
- ✅ El acceso se controla mediante `Partner.user`

---

### 3️⃣ App: `partners` (Socios y Comunidades)

**Propósito:** Gestionar socios de la cooperativa y sus comunidades.

#### Modelo: `Community`

```python
class Community(TenantModel):
    """Comunidades de socios"""
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Heredado de TenantModel:
    # organization = ForeignKey(Organization)
```

#### Modelo: `Partner`

```python
class Partner(TenantModel):
    """Socios de la cooperativa"""
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
        ('SUSPENDED', 'Suspendido'),
    ]
    
    # Información personal
    ci = models.CharField(max_length=10)              # Cédula de Identidad
    nit = models.CharField(max_length=15)             # NIT
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Contacto
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=17)
    address = models.TextField(blank=True)
    
    # Relaciones
    community = models.ForeignKey(Community, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    registration_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    # Heredado de TenantModel:
    # organization = ForeignKey(Organization)
```

**Propiedades Calculadas:**
```python
@property
def full_name(self):
    return f"{self.first_name} {self.last_name}"

@property
def total_parcels(self):
    return self.parcels.count()

@property
def total_surface(self):
    return self.parcels.aggregate(Sum('surface'))['surface__sum'] or 0
```

**Características:**
- ✅ Hereda de `TenantModel` (filtrado automático)
- ✅ Unique constraint: `(organization, ci)` y `(organization, nit)`
- ✅ Relación 1:1 con `User` (opcional)
- ✅ Relación N:1 con `Community`

---

### 4️⃣ App: `parcels` (Parcelas y Cultivos)

**Propósito:** Gestionar parcelas agrícolas, cultivos y tipos de suelo.

#### Modelo: `SoilType`

```python
class SoilType(TenantModel):
    """Tipos de suelo"""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
```

#### Modelo: `Crop`

```python
class Crop(TenantModel):
    """Cultivos"""
    
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
```

#### Modelo: `Parcel`

```python
class Parcel(TenantModel):
    """Parcelas agrícolas"""
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Activa'),
        ('INACTIVE', 'Inactiva'),
    ]
    
    # Información básica
    code = models.CharField(max_length=50)            # Código único
    name = models.CharField(max_length=200)
    surface = models.DecimalField(max_digits=10, decimal_places=2)  # Hectáreas
    
    # Ubicación
    location = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    
    # Relaciones
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    soil_type = models.ForeignKey(SoilType, on_delete=models.PROTECT)
    current_crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True)
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

**Características:**
- ✅ Unique constraint: `(organization, code)`
- ✅ Índices en: `code`, `partner`
- ✅ Relación N:1 con `Partner`
- ✅ Geolocalización con lat/long

---

### 5️⃣ App: `campaigns` (Campañas Agrícolas)

**Propósito:** Gestionar campañas agrícolas y asignación de recursos.

#### Modelo: `Campaign`

```python
class Campaign(TenantModel):
    """Campañas agrícolas"""
    
    STATUS_CHOICES = [
        ('PLANNING', 'En Planificación'),
        ('ACTIVE', 'Activa'),
        ('COMPLETED', 'Completada'),
        ('CANCELLED', 'Cancelada'),
    ]
    
    # Información básica
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Fechas
    start_date = models.DateField()
    end_date = models.DateField()
    actual_end_date = models.DateField(null=True)
    
    # Metas
    target_area = models.DecimalField(max_digits=10, decimal_places=2)
    target_production = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    # Relaciones
    partners = models.ManyToManyField(Partner, related_name='campaigns')
    parcels = models.ManyToManyField(Parcel, related_name='campaigns')
    
    # Metadatos
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

**Propiedades Calculadas:**
```python
@property
def total_area(self):
    """Área total de parcelas asignadas"""
    return self.parcels.aggregate(Sum('surface'))['surface__sum'] or 0

@property
def total_partners(self):
    """Total de socios participantes"""
    return self.partners.count()

@property
def is_active(self):
    """Verifica si la campaña está activa"""
    return self.status == self.ACTIVE
```

**Características:**
- ✅ Unique constraint: `(organization, code)`
- ✅ Relación M:N con `Partner` y `Parcel`
- ✅ Índices en: `code`, `status`, `start_date`

---

### 6️⃣ App: `production` (Productos Cosechados)

**Propósito:** Registrar productos cosechados y su calidad.

#### Modelo: `HarvestedProduct`

```python
class HarvestedProduct(TenantModel):
    """Productos cosechados"""
    
    # Relaciones
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    
    # Detalles del producto
    product_name = models.CharField(max_length=200)
    harvest_date = models.DateField()
    
    # Cantidades
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # kg
    quality_grade = models.CharField(max_length=50, blank=True)
    
    # Condiciones
    moisture_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Almacenamiento
    storage_location = models.CharField(max_length=200, blank=True)
    observations = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

**Propiedades Calculadas:**
```python
@property
def yield_per_hectare(self):
    """Rendimiento por hectárea"""
    if self.parcel.surface > 0:
        return self.quantity / self.parcel.surface
    return 0
```

**Características:**
- ✅ Índices en: `(campaign, harvest_date)`, `parcel`, `partner`
- ✅ Tracking de calidad y condiciones
- ✅ Cálculo automático de rendimiento

---

### 7️⃣ App: `farm_activities` (Labores Agrícolas)

**Propósito:** Registrar labores agrícolas realizadas en las parcelas.

#### Modelo: `ActivityType`

```python
class ActivityType(TenantModel):
    """Tipos de labores agrícolas"""
    
    TYPE_CHOICES = [
        ('SOWING', 'Siembra'),
        ('IRRIGATION', 'Riego'),
        ('FERTILIZATION', 'Fertilización'),
        ('PEST_CONTROL', 'Control de Plagas'),
        ('HARVEST', 'Cosecha'),
        ('OTHER', 'Otra'),
    ]
    
    name = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
```

#### Modelo: `FarmActivity`

```python
class FarmActivity(TenantModel):
    """Labores agrícolas realizadas"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('IN_PROGRESS', 'En Progreso'),
        ('COMPLETED', 'Completada'),
        ('CANCELLED', 'Cancelada'),
    ]
    
    # Información básica
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    
    # Fechas
    scheduled_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    
    # Detalles
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    area_covered = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    # Personal
    workers_count = models.IntegerField(default=1)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    # Observaciones
    observations = models.TextField(blank=True)
    weather_conditions = models.CharField(max_length=200, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

**Características:**
- ✅ Unique constraint: `(organization, name)` para ActivityType
- ✅ Índices en: `(campaign, scheduled_date)`, `(parcel, activity_type)`, `status`
- ✅ Tracking de fechas programadas vs reales
- ✅ Estados: PENDING, IN_PROGRESS, COMPLETED, CANCELLED

---

### 8️⃣ App: `inventory` (Inventario de Insumos)

**Propósito:** Gestionar inventario de insumos agrícolas (semillas, fertilizantes, pesticidas).

#### Modelo: `InventoryCategory`

```python
class InventoryCategory(TenantModel):
    """Categorías de inventario"""
    
    CATEGORY_CHOICES = [
        ('SEED', 'Semilla'),
        ('PESTICIDE', 'Pesticida'),
        ('FERTILIZER', 'Fertilizante'),
        ('TOOL', 'Herramienta'),
        ('OTHER', 'Otro'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
```

#### Modelo: `InventoryItem`

```python
class InventoryItem(TenantModel):
    """Items de inventario"""
    
    # Información básica
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(InventoryCategory, on_delete=models.PROTECT)
    
    # Detalles específicos (para semillas)
    species = models.CharField(max_length=200, blank=True)
    variety = models.CharField(max_length=200, blank=True)
    brand = models.CharField(max_length=200, blank=True)
    germination_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Unidad de medida
    unit_of_measure = models.CharField(max_length=50)  # kg, l, unidades
    
    # Stock
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    # Precio
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    # Vencimiento
    expiration_date = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
```

**Propiedades Calculadas:**
```python
@property
def is_low_stock(self):
    """Verifica si el stock está bajo"""
    return self.current_stock <= self.minimum_stock

@property
def stock_status(self):
    """Estado del stock"""
    if self.current_stock == 0:
        return 'OUT_OF_STOCK'
    elif self.is_low_stock:
        return 'LOW_STOCK'
    return 'NORMAL'
```

#### Modelo: `InventoryMovement`

```python
class InventoryMovement(TenantModel):
    """Movimientos de inventario (entradas y salidas)"""
    
    TYPE_CHOICES = [
        ('ENTRY', 'Entrada'),
        ('EXIT', 'Salida'),
        ('ADJUSTMENT', 'Ajuste'),
    ]
    
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    reference = models.CharField(max_length=200, blank=True)
    reason = models.TextField()
    
    # Costos
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
```

**Características:**
- ✅ Unique constraint: `(organization, code)` para InventoryItem
- ✅ Actualización automática de stock en save() de InventoryMovement
- ✅ Alertas de stock bajo
- ✅ Tracking de vencimientos

---

### 9️⃣ App: `sales` (Ventas y Pedidos)

**Propósito:** Gestionar ventas de productos a clientes.

#### Modelo: `PaymentMethod`

```python
class PaymentMethod(TenantModel):
    """Métodos de pago"""
    
    METHOD_CHOICES = [
        ('CASH', 'Efectivo'),
        ('BANK_TRANSFER', 'Transferencia Bancaria'),
        ('CHECK', 'Cheque'),
        ('CREDIT_CARD', 'Tarjeta de Crédito'),
        ('DEBIT_CARD', 'Tarjeta de Débito'),
        ('QR', 'Código QR'),
        ('OTHER', 'Otro'),
    ]
    
    name = models.CharField(max_length=50, choices=METHOD_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    requires_reference = models.BooleanField(default=False)
```

#### Modelo: `Customer`

```python
class Customer(TenantModel):
    """Clientes (pueden ser socios o externos)"""
    
    # Información básica
    name = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=[
        ('CI', 'CI'), ('NIT', 'NIT'), ('PASSPORT', 'Pasaporte')
    ])
    document_number = models.CharField(max_length=50)
    
    # Contacto
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    
    # Relación con socio (opcional)
    partner = models.OneToOneField(Partner, on_delete=models.SET_NULL, null=True)
    
    is_active = models.BooleanField(default=True)
```

#### Modelo: `Order`

```python
class Order(TenantModel):
    """Pedidos de venta"""
    
    STATUS_CHOICES = [
        ('DRAFT', 'Borrador'),
        ('CONFIRMED', 'Confirmado'),
        ('PAID', 'Pagado'),
        ('SHIPPED', 'Enviado'),
        ('DELIVERED', 'Entregado'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    # Información básica
    order_number = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT)
    
    # Fechas
    order_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    
    # Montos
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True)
```

**Métodos:**
```python
def calculate_totals(self):
    """Calcular totales del pedido"""
    self.subtotal = sum(item.line_total for item in self.items.all())
    self.discount_amount = (self.subtotal * self.discount_percentage) / 100
    self.total = self.subtotal - self.discount_amount + self.tax_amount
    self.save()

@property
def total_items(self):
    return self.items.count()

@property
def total_quantity(self):
    return sum(item.quantity for item in self.items.all())
```

#### Modelo: `OrderItem`

```python
class OrderItem(TenantModel):
    """Items de pedido"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(HarvestedProduct, on_delete=models.PROTECT)
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    notes = models.TextField(blank=True)
```

#### Modelo: `Payment`

```python
class Payment(TenantModel):
    """Pagos de pedidos"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('COMPLETED', 'Completado'),
        ('FAILED', 'Fallido'),
        ('REFUNDED', 'Reembolsado'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    reference_number = models.CharField(max_length=200, blank=True)
    receipt_number = models.CharField(max_length=200, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
```

**Características:**
- ✅ Unique constraint: `(organization, order_number)`, `(organization, document_number)` para Customer
- ✅ Cálculo automático de totales en OrderItem.save()
- ✅ Relación opcional Customer-Partner
- ✅ Múltiples pagos por pedido

---

### 📊 Resumen de Modelos Multi-Tenant

| App | Modelo | Hereda TenantModel | Unique Constraint |
|-----|--------|-------------------|-------------------|
| tenants | Organization | ❌ | subdomain |
| tenants | OrganizationMember | ❌ | (organization, user) |
| users | User | ❌ | email, username |
| users | Role | ❌ | name |
| partners | Community | ✅ | (organization, name) |
| partners | Partner | ✅ | (organization, ci), (organization, nit) |
| parcels | SoilType | ✅ | (organization, name) |
| parcels | Crop | ✅ | (organization, name) |
| parcels | Parcel | ✅ | (organization, code) |
| campaigns | Campaign | ✅ | (organization, code) |
| production | HarvestedProduct | ✅ | - |
| farm_activities | ActivityType | ✅ | (organization, name) |
| farm_activities | FarmActivity | ✅ | - |
| inventory | InventoryCategory | ✅ | (organization, name) |
| inventory | InventoryItem | ✅ | (organization, code) |
| inventory | InventoryMovement | ✅ | - |
| inventory | StockAlert | ✅ | - |
| sales | PaymentMethod | ✅ | (organization, name) |
| sales | Customer | ✅ | (organization, document_number) |
| sales | Order | ✅ | (organization, order_number) |
| sales | OrderItem | ✅ | - |
| sales | Payment | ✅ | - |

---

### 🔗 Relaciones Entre Modelos

```
Organization (tenants)
    ↓ (1:N)
    ├─ Partner (partners)
    │   ↓ (1:N)
    │   ├─ Parcel (parcels)
    │   │   ↓ (1:N)
    │   │   └─ HarvestedProduct (production)
    │   │
    │   └─ FarmActivity (farm_activities)
    │
    ├─ Campaign (campaigns)
    │   ↓ (M:N)
    │   ├─ Partner
    │   └─ Parcel
    │
    ├─ Input (inventory)
    │   ↓ (M:N)
    │   └─ FarmActivity
    │
    └─ Order (sales)
        ↓ (1:N)
        ├─ OrderItem
        └─ Payment (financial)
```

---

**Continúa en PASO 4: Gestión de Organizaciones...**


## 🔧 GESTIÓN DE ORGANIZACIONES (PASO 4)

### Operaciones CRUD de Organizaciones

El sistema permite gestionar organizaciones (cooperativas) de múltiples formas:

1. **Registro Público** - Cualquiera puede registrar una nueva cooperativa
2. **Panel de Super Admin** - Super admin puede crear/editar/eliminar cooperativas
3. **API REST** - Endpoints para gestión programática

---

### 1️⃣ Registro Público de Organizaciones

**Endpoint:** `POST /api/tenants/register/`  
**Permisos:** Público (AllowAny)  
**Propósito:** Permite que cualquier persona registre una nueva cooperativa.

#### Request Body:

```json
{
  "organization_name": "Cooperativa Nueva",
  "subdomain": "cooperativanueva",
  "email": "contacto@cooperativanueva.com",
  "phone": "+54 264 123 4567",
  
  "username": "admin_nueva",
  "user_email": "admin@cooperativanueva.com",
  "password": "password123",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

#### Response (201 Created):

```json
{
  "message": "Organización registrada exitosamente",
  "organization": {
    "id": 5,
    "name": "Cooperativa Nueva",
    "subdomain": "cooperativanueva",
    "plan": "FREE",
    "status": "TRIAL"
  },
  "user": {
    "id": 15,
    "username": "admin_nueva",
    "email": "admin@cooperativanueva.com"
  }
}
```

#### Proceso Automático:

1. **Validaciones:**
   - Subdomain único
   - Username único
   - Email único
   - Password mínimo 8 caracteres

2. **Creación de Organización:**
   - Plan: `FREE`
   - Status: `TRIAL`
   - Trial: 30 días
   - Límites: 5 usuarios, 100 productos, 100 MB

3. **Creación de Usuario:**
   - Usuario propietario (OWNER)
   - Contraseña hasheada
   - Email de bienvenida (opcional)

4. **Membresía:**
   - Relación `OrganizationMember`
   - Role: `OWNER`
   - is_active: `True`

---

### 2️⃣ Panel de Super Admin

**Acceso:** Solo usuarios con `is_superuser=True`

#### Endpoints Disponibles:

```python
# Estadísticas del dashboard
GET /api/tenants/super-admin/stats/

# Listar todas las organizaciones
GET /api/tenants/super-admin/organizations/
GET /api/tenants/super-admin/organizations/?status=ACTIVE
GET /api/tenants/super-admin/organizations/?plan=FREE
GET /api/tenants/super-admin/organizations/?search=san

# Detalle de organización
GET /api/tenants/super-admin/organizations/{id}/

# Crear organización
POST /api/tenants/super-admin/organizations/

# Actualizar organización
PUT /api/tenants/super-admin/organizations/{id}/

# Eliminar organización (soft delete)
DELETE /api/tenants/super-admin/organizations/{id}/
```

---

#### A. Estadísticas del Dashboard

**Endpoint:** `GET /api/tenants/super-admin/stats/`

**Response:**

```json
{
  "organizations": {
    "total": 10,
    "active": 7,
    "trial": 2,
    "suspended": 1,
    "new_last_month": 3
  },
  "users": {
    "total": 45,
    "active": 42
  },
  "plan_distribution": {
    "FREE": 5,
    "BASIC": 3,
    "PROFESSIONAL": 2
  },
  "recent_organizations": [
    {
      "id": 10,
      "name": "Cooperativa Nueva",
      "subdomain": "nueva",
      "plan": "FREE",
      "status": "TRIAL",
      "created_at": "2024-11-20T10:30:00Z",
      "members_count": 1
    }
  ]
}
```

---

#### B. Listar Organizaciones

**Endpoint:** `GET /api/tenants/super-admin/organizations/`

**Query Parameters:**
- `status` - Filtrar por estado (ACTIVE, TRIAL, SUSPENDED, CANCELLED)
- `plan` - Filtrar por plan (FREE, BASIC, PROFESSIONAL, ENTERPRISE)
- `search` - Buscar por nombre, subdominio o email

**Ejemplos:**

```bash
# Todas las organizaciones
GET /api/tenants/super-admin/organizations/

# Solo activas
GET /api/tenants/super-admin/organizations/?status=ACTIVE

# Plan FREE
GET /api/tenants/super-admin/organizations/?plan=FREE

# Buscar "san"
GET /api/tenants/super-admin/organizations/?search=san
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Cooperativa San Juan",
    "subdomain": "sanjuan",
    "email": "contacto@sanjuan.com",
    "phone": "+54 264 123 4567",
    "plan": "FREE",
    "plan_display": "Gratuito",
    "status": "ACTIVE",
    "is_active": true,
    "members_count": 10,
    "max_users": 10,
    "created_at": "2024-01-15T10:00:00Z",
    "trial_ends_at": null,
    "subscription_ends_at": null
  },
  {
    "id": 2,
    "name": "Cooperativa Sypha",
    "subdomain": "syphita",
    "email": "contacto@sypha.com",
    "phone": "",
    "plan": "FREE",
    "plan_display": "Gratuito",
    "status": "TRIAL",
    "is_active": true,
    "members_count": 0,
    "max_users": 5,
    "created_at": "2024-11-20T15:30:00Z",
    "trial_ends_at": "2024-12-20T15:30:00Z",
    "subscription_ends_at": null
  }
]
```

---

#### C. Detalle de Organización

**Endpoint:** `GET /api/tenants/super-admin/organizations/{id}/`

**Response:**

```json
{
  "id": 1,
  "name": "Cooperativa San Juan",
  "slug": "cooperativa-san-juan",
  "subdomain": "sanjuan",
  "email": "contacto@sanjuan.com",
  "phone": "+54 264 123 4567",
  "address": "Calle Principal 123, San Juan",
  "plan": "FREE",
  "plan_display": "Gratuito",
  "status": "ACTIVE",
  "is_active": true,
  "max_users": 10,
  "max_products": 100,
  "max_storage_mb": 1000,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-11-20T12:00:00Z",
  "trial_ends_at": null,
  "subscription_ends_at": null,
  "settings": {},
  "members": [
    {
      "id": 1,
      "user_id": 5,
      "username": "admin_sanjuan",
      "email": "admin@sanjuan.com",
      "full_name": "Juan Pérez",
      "role": "OWNER",
      "is_active": true,
      "joined_at": "2024-01-15T10:00:00Z"
    },
    {
      "id": 2,
      "user_id": 8,
      "username": "socio1",
      "email": "socio1@sanjuan.com",
      "full_name": "María López",
      "role": "MEMBER",
      "is_active": true,
      "joined_at": "2024-02-01T14:30:00Z"
    }
  ],
  "members_count": 2
}
```

---

#### D. Crear Organización (Super Admin)

**Endpoint:** `POST /api/tenants/super-admin/organizations/`

**Request Body:**

```json
{
  "organization_name": "Cooperativa Demo",
  "subdomain": "demo",
  "email": "contacto@demo.com",
  "phone": "+54 264 999 8888",
  
  "username": "admin_demo",
  "user_email": "admin@demo.com",
  "password": "demo123456",
  "first_name": "Admin",
  "last_name": "Demo"
}
```

**Response (201 Created):**

```json
{
  "message": "Organización creada exitosamente",
  "organization": {
    "id": 11,
    "name": "Cooperativa Demo",
    "subdomain": "demo",
    "plan": "FREE",
    "status": "TRIAL"
  },
  "user": {
    "id": 50,
    "username": "admin_demo",
    "email": "admin@demo.com"
  }
}
```

---

#### E. Actualizar Organización

**Endpoint:** `PUT /api/tenants/super-admin/organizations/{id}/`

**Request Body (campos opcionales):**

```json
{
  "name": "Cooperativa San Juan Actualizada",
  "email": "nuevo@sanjuan.com",
  "phone": "+54 264 111 2222",
  "plan": "BASIC",
  "status": "ACTIVE",
  "is_active": true,
  "max_users": 20,
  "max_products": 500,
  "max_storage_mb": 5000
}
```

**Response:**

```json
{
  "message": "Organización actualizada exitosamente",
  "organization": {
    "id": 1,
    "name": "Cooperativa San Juan Actualizada",
    "plan": "BASIC",
    "status": "ACTIVE",
    "is_active": true
  }
}
```

---

#### F. Eliminar Organización (Soft Delete)

**Endpoint:** `DELETE /api/tenants/super-admin/organizations/{id}/`

**Comportamiento:**
- NO elimina físicamente la organización
- Establece `is_active = False`
- Establece `status = 'CANCELLED'`
- Los datos se conservan para auditoría

**Response:**

```json
{
  "message": "Organización Cooperativa San Juan desactivada exitosamente"
}
```

---

### 3️⃣ Mis Organizaciones (Usuario)

**Endpoint:** `GET /api/tenants/my-organizations/`  
**Permisos:** Autenticado  
**Propósito:** Lista las organizaciones donde el usuario es miembro.

**Response:**

```json
[
  {
    "id": 1,
    "name": "Cooperativa San Juan",
    "subdomain": "sanjuan",
    "plan": "FREE",
    "status": "ACTIVE",
    "role": "OWNER",
    "is_active": true
  },
  {
    "id": 3,
    "name": "Cooperativa El Progreso",
    "subdomain": "progreso",
    "plan": "BASIC",
    "status": "ACTIVE",
    "role": "MEMBER",
    "is_active": true
  }
]
```

---

### 4️⃣ Planes y Límites

#### Planes Disponibles:

| Plan | Precio | Usuarios | Productos | Almacenamiento |
|------|--------|----------|-----------|----------------|
| FREE | Gratis | 5 | 100 | 100 MB |
| BASIC | $29/mes | 20 | 500 | 1 GB |
| PROFESSIONAL | $99/mes | 100 | 2000 | 10 GB |
| ENTERPRISE | Custom | Ilimitado | Ilimitado | Ilimitado |

#### Estados de Organización:

| Estado | Descripción | Acceso |
|--------|-------------|--------|
| TRIAL | Período de prueba (30 días) | ✅ Completo |
| ACTIVE | Suscripción activa | ✅ Completo |
| SUSPENDED | Suspendida (falta de pago) | ⚠️ Solo lectura |
| CANCELLED | Cancelada | ❌ Sin acceso |

---

### 5️⃣ Modelo OrganizationMember

**Propósito:** Relaciona usuarios con organizaciones y define sus roles.

```python
class OrganizationMember(models.Model):
    """Membresía de usuario en organización"""
    
    ROLE_CHOICES = [
        ('OWNER', 'Propietario'),
        ('ADMIN', 'Administrador'),
        ('MEMBER', 'Miembro'),
    ]
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
```

**Roles:**
- **OWNER** - Propietario (creador de la organización)
- **ADMIN** - Administrador (puede gestionar la organización)
- **MEMBER** - Miembro (acceso básico)

---

### 6️⃣ Ejemplos de Uso

#### Ejemplo 1: Crear Organización desde Frontend

```javascript
// Frontend - Registro de nueva cooperativa
const registerOrganization = async (formData) => {
  const response = await fetch('http://localhost:8000/api/tenants/register/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      organization_name: formData.orgName,
      subdomain: formData.subdomain,
      email: formData.email,
      phone: formData.phone,
      username: formData.username,
      user_email: formData.userEmail,
      password: formData.password,
      first_name: formData.firstName,
      last_name: formData.lastName
    })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    console.log('Organización creada:', data.organization);
    console.log('Usuario creado:', data.user);
    // Redirigir al login
    window.location.href = '/login';
  } else {
    console.error('Errores:', data);
  }
};
```

---

#### Ejemplo 2: Listar Mis Organizaciones

```javascript
// Frontend - Obtener organizaciones del usuario
const getMyOrganizations = async () => {
  const response = await fetch('http://localhost:8000/api/tenants/my-organizations/', {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    }
  });
  
  const organizations = await response.json();
  
  // Mostrar selector de organizaciones
  organizations.forEach(org => {
    console.log(`${org.name} (${org.subdomain}) - Role: ${org.role}`);
  });
};
```

---

#### Ejemplo 3: Super Admin - Actualizar Plan

```javascript
// Frontend - Super Admin actualiza plan de organización
const upgradePlan = async (orgId, newPlan) => {
  const response = await fetch(
    `http://localhost:8000/api/tenants/super-admin/organizations/${orgId}/`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${superAdminToken}`,
      },
      body: JSON.stringify({
        plan: newPlan,
        max_users: newPlan === 'BASIC' ? 20 : 100,
        max_products: newPlan === 'BASIC' ? 500 : 2000,
        max_storage_mb: newPlan === 'BASIC' ? 1024 : 10240
      })
    }
  );
  
  const data = await response.json();
  console.log('Plan actualizado:', data);
};
```

---

### 7️⃣ Validaciones y Reglas de Negocio

#### Validaciones en Registro:

1. **Subdomain:**
   - Solo letras minúsculas, números y guiones
   - Único en el sistema
   - Mínimo 3 caracteres

2. **Email:**
   - Formato válido
   - Único para organizaciones

3. **Username:**
   - Único en el sistema
   - Mínimo 3 caracteres

4. **Password:**
   - Mínimo 8 caracteres
   - Se hashea con bcrypt

#### Reglas de Negocio:

1. **Trial Automático:**
   - Nuevas organizaciones: 30 días de prueba
   - Plan FREE con límites reducidos

2. **Límites por Plan:**
   - Se validan al crear usuarios/productos
   - Se pueden aumentar al mejorar plan

3. **Soft Delete:**
   - Las organizaciones no se eliminan físicamente
   - Se desactivan para mantener auditoría

4. **Membresía Única:**
   - Un usuario puede pertenecer a múltiples organizaciones
   - Pero solo una membresía activa por organización

---

### 8️⃣ Scripts de Gestión

#### Script: Crear Organización de Prueba

```python
# Backend/create_test_organization.py
from tenants.models import Organization, OrganizationMember
from users.models import User
from datetime import timedelta
from django.utils import timezone

def create_test_organization():
    # Crear organización
    org = Organization.objects.create(
        name='Cooperativa Test',
        subdomain='test',
        email='test@cooperativa.com',
        plan='FREE',
        status='TRIAL',
        trial_ends_at=timezone.now() + timedelta(days=30),
        max_users=5,
        max_products=100,
        max_storage_mb=100
    )
    
    # Crear usuario propietario
    user = User.objects.create_user(
        username='admin_test',
        email='admin@test.com',
        password='test123',
        first_name='Admin',
        last_name='Test'
    )
    
    # Crear membresía
    OrganizationMember.objects.create(
        organization=org,
        user=user,
        role='OWNER',
        is_active=True
    )
    
    print(f"✅ Organización creada: {org.name}")
    print(f"   Subdomain: {org.subdomain}")
    print(f"   Usuario: {user.username}")
    print(f"   URL: http://{org.subdomain}.localhost:8000/")

if __name__ == '__main__':
    create_test_organization()
```

---

**Continúa en PASO 5: Ejemplos Prácticos...**


## 💡 EJEMPLOS PRÁCTICOS (PASO 5)

### Casos de Uso Reales del Sistema Multi-Tenant

---

### 1️⃣ Caso de Uso: Registro de Nueva Cooperativa

**Escenario:** Una nueva cooperativa quiere usar el sistema.

#### Flujo Completo:

```
Usuario → Landing Page → Formulario de Registro → Confirmación → Login
```

#### Paso 1: Usuario completa formulario

```javascript
// Frontend/src/pages/RegisterPage.jsx
const handleSubmit = async (e) => {
  e.preventDefault();
  
  const formData = {
    organization_name: "Cooperativa El Progreso",
    subdomain: "progreso",
    email: "contacto@progreso.com",
    phone: "+54 264 555 1234",
    
    username: "admin_progreso",
    user_email: "admin@progreso.com",
    password: "progreso2024",
    first_name: "Carlos",
    last_name: "Rodríguez"
  };
  
  try {
    const response = await fetch('http://localhost:8000/api/tenants/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    
    if (response.ok) {
      const data = await response.json();
      alert(`¡Cooperativa ${data.organization.name} creada exitosamente!`);
      // Redirigir al login
      window.location.href = '/login';
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
```

#### Paso 2: Backend crea organización

```python
# Backend/tenants/serializers.py
def create(self, validated_data):
    # 1. Crear organización
    organization = Organization.objects.create(
        name='Cooperativa El Progreso',
        subdomain='progreso',
        email='contacto@progreso.com',
        plan='FREE',
        status='TRIAL',
        trial_ends_at=timezone.now() + timedelta(days=30)
    )
    
    # 2. Crear usuario propietario
    user = User.objects.create_user(
        username='admin_progreso',
        email='admin@progreso.com',
        password='progreso2024'
    )
    
    # 3. Crear membresía
    OrganizationMember.objects.create(
        organization=organization,
        user=user,
        role='OWNER'
    )
    
    return {'organization': organization, 'user': user}
```

#### Paso 3: Usuario hace login

```javascript
// Frontend - Login con organización
const login = async () => {
  const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Organization-Subdomain': 'progreso'  // ← Especifica la organización
    },
    body: JSON.stringify({
      username: 'admin_progreso',
      password: 'progreso2024'
    })
  });
  
  const data = await response.json();
  // Guardar token y organización
  localStorage.setItem('accessToken', data.access);
  localStorage.setItem('currentOrganization', 'progreso');
};
```

**Resultado:**
- ✅ Organización creada con plan FREE (30 días de prueba)
- ✅ Usuario propietario creado
- ✅ Puede empezar a usar el sistema inmediatamente

---

### 2️⃣ Caso de Uso: Agregar Socio a la Cooperativa

**Escenario:** Admin de "Cooperativa San Juan" agrega un nuevo socio.

#### Flujo Completo:

```
Admin Login → Dashboard → Socios → Nuevo Socio → Guardar
```

#### Paso 1: Admin hace request

```javascript
// Frontend - Crear nuevo socio
const createPartner = async (partnerData) => {
  const response = await fetch('http://localhost:8000/api/partners/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      'X-Organization-Subdomain': 'sanjuan'  // ← Organización actual
    },
    body: JSON.stringify({
      ci: '12345678',
      nit: '12345678012',
      first_name: 'Pedro',
      last_name: 'García',
      email: 'pedro@example.com',
      phone: '+54 264 111 2222',
      community: 1,  // ID de comunidad
      status: 'ACTIVE'
    })
  });
  
  const partner = await response.json();
  console.log('Socio creado:', partner);
};
```

#### Paso 2: Middleware detecta organización

```python
# Backend/tenants/middleware.py
def process_request(self, request):
    # Lee header
    subdomain = request.headers.get('X-Organization-Subdomain')  # 'sanjuan'
    
    # Busca organización
    organization = Organization.objects.get(subdomain=subdomain)
    
    # Guarda en thread-local
    set_current_organization(organization)
```

#### Paso 3: Manager filtra automáticamente

```python
# Backend/partners/views.py
class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()  # ← TenantManager filtra automáticamente
    
    def perform_create(self, serializer):
        # organization se asigna automáticamente por TenantModel.save()
        serializer.save()
```

#### Paso 4: Query SQL ejecutada

```sql
-- El TenantManager genera esta query:
INSERT INTO partners_partner (
    organization_id,  -- ← Auto-asignado = 1 (San Juan)
    ci,
    first_name,
    last_name,
    ...
) VALUES (
    1,  -- ← ID de "Cooperativa San Juan"
    '12345678',
    'Pedro',
    'García',
    ...
);
```

**Resultado:**
- ✅ Socio creado en organización correcta
- ✅ Imposible crear socio en otra organización por error
- ✅ Filtrado automático en todas las queries

---

### 3️⃣ Caso de Uso: Listar Socios (Aislamiento de Datos)

**Escenario:** Dos cooperativas listan sus socios simultáneamente.

#### Request 1: Cooperativa San Juan

```javascript
// Usuario de San Juan
fetch('http://localhost:8000/api/partners/', {
  headers: {
    'Authorization': 'Bearer token_sanjuan',
    'X-Organization-Subdomain': 'sanjuan'
  }
});
```

**Query SQL generada:**
```sql
SELECT * FROM partners_partner
WHERE organization_id = 1;  -- San Juan
```

**Resultado:**
```json
[
  {"id": 1, "name": "Juan Pérez", "organization": 1},
  {"id": 2, "name": "María López", "organization": 1},
  {"id": 3, "name": "Pedro García", "organization": 1}
]
```

---

#### Request 2: Cooperativa Sypha (simultánea)

```javascript
// Usuario de Sypha
fetch('http://localhost:8000/api/partners/', {
  headers: {
    'Authorization': 'Bearer token_sypha',
    'X-Organization-Subdomain': 'syphita'
  }
});
```

**Query SQL generada:**
```sql
SELECT * FROM partners_partner
WHERE organization_id = 2;  -- Sypha
```

**Resultado:**
```json
[]  // Vacío - Sypha no tiene socios aún
```

**Conclusión:**
- ✅ Cada cooperativa ve SOLO sus datos
- ✅ Requests simultáneas no interfieren
- ✅ Aislamiento garantizado por middleware + manager

---

### 4️⃣ Caso de Uso: Super Admin Gestiona Cooperativas

**Escenario:** Super admin revisa todas las cooperativas y actualiza una.

#### Paso 1: Ver estadísticas globales

```javascript
// Frontend - Dashboard de Super Admin
const loadStats = async () => {
  const response = await fetch(
    'http://localhost:8000/api/tenants/super-admin/stats/',
    {
      headers: {
        'Authorization': `Bearer ${superAdminToken}`
      }
    }
  );
  
  const stats = await response.json();
  /*
  {
    "organizations": {
      "total": 10,
      "active": 7,
      "trial": 2,
      "suspended": 1
    },
    "users": {
      "total": 45,
      "active": 42
    }
  }
  */
};
```

#### Paso 2: Listar todas las cooperativas

```javascript
// Frontend - Tabla de organizaciones
const loadOrganizations = async () => {
  const response = await fetch(
    'http://localhost:8000/api/tenants/super-admin/organizations/',
    {
      headers: {
        'Authorization': `Bearer ${superAdminToken}`
      }
    }
  );
  
  const organizations = await response.json();
  // Muestra tabla con todas las cooperativas
};
```

#### Paso 3: Actualizar plan de una cooperativa

```javascript
// Frontend - Upgrade de plan
const upgradePlan = async (orgId) => {
  const response = await fetch(
    `http://localhost:8000/api/tenants/super-admin/organizations/${orgId}/`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${superAdminToken}`
      },
      body: JSON.stringify({
        plan: 'BASIC',
        max_users: 20,
        max_products: 500,
        max_storage_mb: 1024
      })
    }
  );
  
  const result = await response.json();
  alert('Plan actualizado exitosamente');
};
```

**Resultado:**
- ✅ Super admin ve todas las organizaciones
- ✅ Puede actualizar planes y límites
- ✅ Puede suspender/activar cooperativas

---

### 5️⃣ Caso de Uso: Usuario con Múltiples Organizaciones

**Escenario:** Un usuario es miembro de 2 cooperativas diferentes.

#### Paso 1: Listar mis organizaciones

```javascript
// Frontend - Selector de organizaciones
const getMyOrganizations = async () => {
  const response = await fetch(
    'http://localhost:8000/api/tenants/my-organizations/',
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
  
  const organizations = await response.json();
  /*
  [
    {
      "id": 1,
      "name": "Cooperativa San Juan",
      "subdomain": "sanjuan",
      "role": "OWNER"
    },
    {
      "id": 3,
      "name": "Cooperativa El Progreso",
      "subdomain": "progreso",
      "role": "MEMBER"
    }
  ]
  */
  
  // Mostrar selector
  return organizations;
};
```

#### Paso 2: Cambiar de organización

```javascript
// Frontend - Cambio de contexto
const switchOrganization = (subdomain) => {
  // Guardar organización actual
  localStorage.setItem('currentOrganization', subdomain);
  
  // Recargar página para limpiar estado
  window.location.reload();
};
```

#### Paso 3: Hacer requests con nueva organización

```javascript
// Todas las requests posteriores usan la nueva organización
const loadData = async () => {
  const currentOrg = localStorage.getItem('currentOrganization');
  
  const response = await fetch('http://localhost:8000/api/partners/', {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'X-Organization-Subdomain': currentOrg  // ← Organización actual
    }
  });
  
  // Datos de la organización seleccionada
};
```

**Resultado:**
- ✅ Usuario puede acceder a múltiples cooperativas
- ✅ Cambio de contexto simple y seguro
- ✅ Datos siempre filtrados por organización actual

---

### 6️⃣ Caso de Uso: Registrar Cosecha

**Escenario:** Socio registra una cosecha en su parcela.

#### Flujo Completo:

```javascript
// Frontend - Registrar cosecha
const registerHarvest = async () => {
  const harvestData = {
    campaign: 1,           // ID de campaña
    parcel: 5,             // ID de parcela del socio
    partner: 3,            // ID del socio
    product_name: 'Maíz',
    harvest_date: '2024-11-20',
    quantity: 1500,        // kg
    quality_grade: 'A',
    moisture_percentage: 14.5,
    storage_location: 'Almacén Central'
  };
  
  const response = await fetch(
    'http://localhost:8000/api/production/harvested-products/',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
        'X-Organization-Subdomain': 'sanjuan'
      },
      body: JSON.stringify(harvestData)
    }
  );
  
  const harvest = await response.json();
  console.log('Cosecha registrada:', harvest);
};
```

#### Backend procesa:

```python
# Backend/production/views.py
class HarvestedProductViewSet(viewsets.ModelViewSet):
    queryset = HarvestedProduct.objects.all()  # ← Filtrado automático
    
    def perform_create(self, serializer):
        # organization se asigna automáticamente
        harvest = serializer.save()
        
        # Calcular rendimiento
        yield_per_ha = harvest.yield_per_hectare
        print(f"Rendimiento: {yield_per_ha} kg/ha")
```

#### Query SQL:

```sql
INSERT INTO production_harvestedproduct (
    organization_id,  -- ← Auto-asignado = 1
    campaign_id,
    parcel_id,
    partner_id,
    product_name,
    quantity,
    ...
) VALUES (
    1,  -- Cooperativa San Juan
    1,
    5,
    3,
    'Maíz',
    1500,
    ...
);
```

**Resultado:**
- ✅ Cosecha registrada en organización correcta
- ✅ Solo visible para miembros de esa cooperativa
- ✅ Cálculos automáticos (rendimiento por hectárea)

---

### 7️⃣ Caso de Uso: Reportes por Organización

**Escenario:** Admin genera reporte de producción de su cooperativa.

#### Request:

```javascript
// Frontend - Reporte de producción
const getProductionReport = async () => {
  const response = await fetch(
    'http://localhost:8000/api/reports/production-by-parcel/',
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'X-Organization-Subdomain': 'sanjuan'
      }
    }
  );
  
  const report = await response.json();
  /*
  [
    {
      "parcel_code": "P001",
      "parcel_name": "Parcela Norte",
      "partner_name": "Juan Pérez",
      "total_production": 3500,
      "average_yield": 2800
    },
    {
      "parcel_code": "P002",
      "parcel_name": "Parcela Sur",
      "partner_name": "María López",
      "total_production": 4200,
      "average_yield": 3100
    }
  ]
  */
};
```

#### Backend genera reporte:

```python
# Backend/reports/views.py
@api_view(['GET'])
def production_by_parcel(request):
    # HarvestedProduct.objects ya está filtrado por organización
    products = HarvestedProduct.objects.select_related(
        'parcel', 'partner'
    ).values(
        'parcel__code',
        'parcel__name',
        'partner__first_name',
        'partner__last_name'
    ).annotate(
        total_production=Sum('quantity'),
        average_yield=Avg('quantity')
    )
    
    return Response(products)
```

**Query SQL:**

```sql
SELECT 
    p.code,
    p.name,
    pt.first_name,
    pt.last_name,
    SUM(hp.quantity) as total_production,
    AVG(hp.quantity) as average_yield
FROM production_harvestedproduct hp
JOIN parcels_parcel p ON hp.parcel_id = p.id
JOIN partners_partner pt ON hp.partner_id = pt.id
WHERE hp.organization_id = 1  -- ← Filtro automático
GROUP BY p.code, p.name, pt.first_name, pt.last_name;
```

**Resultado:**
- ✅ Reporte solo con datos de la cooperativa
- ✅ Agregaciones correctas por organización
- ✅ Imposible ver datos de otras cooperativas

---

### 8️⃣ Caso de Uso: Validación de Acceso

**Escenario:** Usuario intenta acceder a datos de otra organización.

#### Intento de acceso no autorizado:

```javascript
// Usuario de "Sypha" intenta acceder a datos de "San Juan"
fetch('http://localhost:8000/api/partners/', {
  headers: {
    'Authorization': 'Bearer token_sypha_user',
    'X-Organization-Subdomain': 'sanjuan'  // ← Organización diferente
  }
});
```

#### Middleware valida acceso:

```python
# Backend/tenants/middleware.py
def process_request(self, request):
    organization = Organization.objects.get(subdomain='sanjuan')
    
    # Verificar acceso del usuario
    if request.user.is_authenticated:
        # Verificar si tiene partner en esta organización
        has_access = Partner.objects.all_organizations().filter(
            organization=organization,
            user=request.user
        ).exists()
        
        if not has_access:
            return JsonResponse({
                'error': 'Acceso denegado',
                'detail': 'No tienes acceso a Cooperativa San Juan'
            }, status=403)
```

**Response:**

```json
{
  "error": "Acceso denegado",
  "detail": "No tienes acceso a Cooperativa San Juan"
}
```

**Resultado:**
- ✅ Acceso bloqueado
- ✅ Usuario solo puede acceder a sus organizaciones
- ✅ Seguridad garantizada por middleware

---

### 9️⃣ Caso de Uso: Migración de Datos

**Escenario:** Importar datos existentes a una nueva cooperativa.

#### Script de migración:

```python
# Backend/scripts/import_data.py
from tenants.models import Organization
from partners.models import Partner, Community
from tenants.middleware import set_current_organization

def import_partners_from_csv(org_subdomain, csv_file):
    # 1. Obtener organización
    org = Organization.objects.get(subdomain=org_subdomain)
    
    # 2. Establecer contexto (importante!)
    set_current_organization(org)
    
    # 3. Crear comunidad
    community = Community.objects.create(
        name='Comunidad Principal',
        # organization se asigna automáticamente
    )
    
    # 4. Importar socios
    import csv
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Partner.objects.create(
                ci=row['ci'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                phone=row['phone'],
                community=community,
                # organization se asigna automáticamente
            )
    
    print(f"✅ Datos importados a {org.name}")

# Uso:
import_partners_from_csv('sanjuan', 'socios_sanjuan.csv')
```

**Resultado:**
- ✅ Datos importados a organización correcta
- ✅ `organization_id` asignado automáticamente
- ✅ Aislamiento garantizado

---

### 🔟 Caso de Uso: Testing Multi-Tenant

**Escenario:** Escribir tests para verificar aislamiento de datos.

#### Test de aislamiento:

```python
# Backend/partners/tests.py
from django.test import TestCase
from tenants.models import Organization
from partners.models import Partner, Community
from tenants.middleware import set_current_organization

class MultiTenantTest(TestCase):
    def setUp(self):
        # Crear dos organizaciones
        self.org1 = Organization.objects.create(
            name='Org 1',
            subdomain='org1'
        )
        self.org2 = Organization.objects.create(
            name='Org 2',
            subdomain='org2'
        )
    
    def test_data_isolation(self):
        # Crear datos en org1
        set_current_organization(self.org1)
        community1 = Community.objects.create(name='Community 1')
        partner1 = Partner.objects.create(
            ci='111',
            first_name='Partner',
            last_name='One',
            community=community1
        )
        
        # Crear datos en org2
        set_current_organization(self.org2)
        community2 = Community.objects.create(name='Community 2')
        partner2 = Partner.objects.create(
            ci='222',
            first_name='Partner',
            last_name='Two',
            community=community2
        )
        
        # Verificar aislamiento
        set_current_organization(self.org1)
        partners_org1 = Partner.objects.all()
        self.assertEqual(partners_org1.count(), 1)
        self.assertEqual(partners_org1.first().ci, '111')
        
        set_current_organization(self.org2)
        partners_org2 = Partner.objects.all()
        self.assertEqual(partners_org2.count(), 1)
        self.assertEqual(partners_org2.first().ci, '222')
        
        print("✅ Test de aislamiento pasado")
```

**Resultado:**
- ✅ Datos completamente aislados
- ✅ Queries filtradas correctamente
- ✅ Sistema multi-tenant funciona correctamente

---

**Continúa en PASO 6: Troubleshooting...**


## 🐛 TROUBLESHOOTING (PASO 6)

### Problemas Comunes y Soluciones

---

### ❌ Problema 1: "Organización no encontrada"

**Error:**
```json
{
  "error": "Organización no encontrada",
  "detail": "Debe especificar una organización válida"
}
```

**Causas Posibles:**

1. **No se envía el header `X-Organization-Subdomain`**
2. **El subdomain es incorrecto**
3. **La organización está inactiva**

**Soluciones:**

#### Solución 1: Verificar header en frontend

```javascript
// ❌ MAL - Sin header
fetch('http://localhost:8000/api/partners/');

// ✅ BIEN - Con header
fetch('http://localhost:8000/api/partners/', {
  headers: {
    'X-Organization-Subdomain': 'sanjuan'
  }
});
```

#### Solución 2: Verificar que la organización existe

```bash
# Backend - Verificar organizaciones
cd Backend
python check_org_data.py

# Resultado:
# • Cooperativa San Juan (sanjuan): 10 socios
# • Cooperativa Sypha (syphita): 0 socios
```

#### Solución 3: Verificar que está activa

```python
# Backend - Django shell
python manage.py shell

from tenants.models import Organization
org = Organization.objects.get(subdomain='sanjuan')
print(f"Activa: {org.is_active}")
print(f"Estado: {org.status}")

# Si está inactiva, activar:
org.is_active = True
org.status = 'ACTIVE'
org.save()
```

---

### ❌ Problema 2: "Acceso denegado"

**Error:**
```json
{
  "error": "Acceso denegado",
  "detail": "No tienes acceso a la organización Cooperativa San Juan"
}
```

**Causa:** El usuario no tiene membresía en esa organización.

**Soluciones:**

#### Solución 1: Verificar membresías del usuario

```python
# Backend - Django shell
from users.models import User
from tenants.models import OrganizationMember

user = User.objects.get(username='usuario_test')

# Ver organizaciones del usuario
memberships = OrganizationMember.objects.filter(user=user)
for m in memberships:
    print(f"- {m.organization.name} ({m.role})")
```

#### Solución 2: Agregar usuario a la organización

```python
# Backend - Django shell
from tenants.models import Organization, OrganizationMember
from users.models import User

org = Organization.objects.get(subdomain='sanjuan')
user = User.objects.get(username='usuario_test')

# Crear membresía
OrganizationMember.objects.create(
    organization=org,
    user=user,
    role='MEMBER',
    is_active=True
)

print(f"✅ Usuario agregado a {org.name}")
```

#### Solución 3: Crear Partner para el usuario

```python
# Backend - Django shell
from partners.models import Partner, Community
from tenants.middleware import set_current_organization

# Establecer contexto
set_current_organization(org)

# Crear partner
community = Community.objects.first()
partner = Partner.objects.create(
    ci='12345678',
    first_name=user.first_name,
    last_name=user.last_name,
    email=user.email,
    phone='+54 264 111 2222',
    community=community,
    user=user
)

print(f"✅ Partner creado para {user.username}")
```

---

### ❌ Problema 3: Todas las organizaciones ven los mismos datos

**Síntoma:** Cooperativa A ve datos de Cooperativa B.

**Causa:** El middleware NO está filtrando correctamente.

**Diagnóstico:**

```python
# Backend - Verificar datos
cd Backend
python check_org_data.py sanjuan
python check_org_data.py syphita

# Si ambos muestran los mismos datos, hay un problema
```

**Soluciones:**

#### Solución 1: Verificar que el middleware está activo

```python
# Backend/config/settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # ⚠️ DEBE ESTAR AQUÍ
    'tenants.middleware.TenantMiddleware',  # ← Verificar
]
```

#### Solución 2: Verificar que los modelos heredan de TenantModel

```python
# Backend/partners/models.py
from tenants.managers import TenantModel

# ❌ MAL
class Partner(models.Model):
    organization = models.ForeignKey(Organization)
    # ...

# ✅ BIEN
class Partner(TenantModel):  # ← Hereda de TenantModel
    # organization ya está incluido
    # ...
```

#### Solución 3: Verificar que los datos tienen organization_id

```sql
-- Backend - Verificar en la base de datos
SELECT id, first_name, organization_id 
FROM partners_partner 
LIMIT 10;

-- Si organization_id es NULL, hay un problema
```

#### Solución 4: Asignar organization_id a datos existentes

```python
# Backend - Script de corrección
from tenants.models import Organization
from partners.models import Partner

# Obtener organización por defecto
org = Organization.objects.get(subdomain='sanjuan')

# Actualizar partners sin organización
partners_sin_org = Partner.objects.all_organizations().filter(
    organization__isnull=True
)

for partner in partners_sin_org:
    partner.organization = org
    partner.save()

print(f"✅ {partners_sin_org.count()} partners actualizados")
```

---

### ❌ Problema 4: Error al crear registro sin organización

**Error:**
```
ValueError: No se puede guardar Partner sin una organización.
Asegúrate de que el middleware TenantMiddleware esté configurado.
```

**Causa:** No hay organización en el contexto (thread-local).

**Soluciones:**

#### Solución 1: Establecer organización en scripts

```python
# Backend - Script
from tenants.models import Organization
from tenants.middleware import set_current_organization
from partners.models import Partner

# ❌ MAL - Sin establecer contexto
partner = Partner.objects.create(...)  # Error!

# ✅ BIEN - Con contexto
org = Organization.objects.get(subdomain='sanjuan')
set_current_organization(org)

partner = Partner.objects.create(...)  # Funciona!
```

#### Solución 2: Asignar organización manualmente

```python
# Backend - Alternativa
org = Organization.objects.get(subdomain='sanjuan')

partner = Partner.objects.create(
    organization=org,  # ← Asignar manualmente
    ci='12345678',
    # ...
)
```

---

### ❌ Problema 5: Frontend muestra datos de organización anterior

**Síntoma:** Después de cambiar de organización, sigue mostrando datos viejos.

**Causa:** Caché del navegador o localStorage.

**Soluciones:**

#### Solución 1: Limpiar localStorage al cambiar

```javascript
// Frontend - Cambio de organización
const switchOrganization = (subdomain) => {
  // Limpiar TODO el localStorage
  localStorage.clear();
  
  // Establecer nueva organización
  localStorage.setItem('currentOrganization', subdomain);
  
  // Recargar página
  window.location.reload();
};
```

#### Solución 2: Usar modo incógnito para testing

```
1. Abrir Chrome en modo incógnito (Ctrl + Shift + N)
2. Navegar a la aplicación
3. Hacer login
4. Verificar datos
```

#### Solución 3: Forzar recarga sin caché

```
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

---

### ❌ Problema 6: Error de unique constraint

**Error:**
```
IntegrityError: duplicate key value violates unique constraint 
"partners_partner_organization_id_ci_key"
```

**Causa:** Intentando crear un socio con CI duplicado en la misma organización.

**Soluciones:**

#### Solución 1: Verificar si ya existe

```python
# Backend - Verificar antes de crear
from partners.models import Partner

ci = '12345678'

# Verificar si existe
if Partner.objects.filter(ci=ci).exists():
    print(f"❌ Ya existe un socio con CI {ci}")
else:
    partner = Partner.objects.create(ci=ci, ...)
    print(f"✅ Socio creado")
```

#### Solución 2: Usar get_or_create

```python
# Backend - Crear o obtener existente
partner, created = Partner.objects.get_or_create(
    ci='12345678',
    defaults={
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'community': community,
        # ...
    }
)

if created:
    print(f"✅ Socio creado")
else:
    print(f"ℹ️ Socio ya existía")
```

---

### ❌ Problema 7: Queries lentas

**Síntoma:** Las consultas tardan mucho tiempo.

**Causa:** Falta de índices o queries N+1.

**Soluciones:**

#### Solución 1: Verificar índices

```python
# Backend/partners/models.py
class Partner(TenantModel):
    # ...
    
    class Meta:
        indexes = [
            models.Index(fields=['ci']),  # ← Índice en CI
            models.Index(fields=['status']),  # ← Índice en status
        ]
        unique_together = [
            ['organization', 'ci'],  # ← Índice compuesto
        ]
```

#### Solución 2: Usar select_related y prefetch_related

```python
# Backend - Optimizar queries

# ❌ MAL - Query N+1
partners = Partner.objects.all()
for partner in partners:
    print(partner.community.name)  # Query por cada partner!

# ✅ BIEN - Una sola query
partners = Partner.objects.select_related('community').all()
for partner in partners:
    print(partner.community.name)  # Sin queries adicionales
```

#### Solución 3: Usar Django Debug Toolbar

```python
# Backend/config/settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Ver queries en el navegador
```

---

### ❌ Problema 8: Migraciones fallan

**Error:**
```
django.db.utils.ProgrammingError: relation "partners_partner" does not exist
```

**Causa:** Migraciones no aplicadas o en orden incorrecto.

**Soluciones:**

#### Solución 1: Aplicar todas las migraciones

```bash
# Backend
python manage.py makemigrations
python manage.py migrate
```

#### Solución 2: Verificar estado de migraciones

```bash
# Backend - Ver migraciones pendientes
python manage.py showmigrations

# Resultado:
# tenants
#  [X] 0001_initial
#  [X] 0002_add_fields
# partners
#  [X] 0001_initial
#  [ ] 0002_add_community  ← Pendiente
```

#### Solución 3: Migrar app específica

```bash
# Backend - Migrar solo partners
python manage.py migrate partners
```

---

### ❌ Problema 9: CORS errors en frontend

**Error:**
```
Access to fetch at 'http://localhost:8000/api/partners/' from origin 
'http://localhost:5173' has been blocked by CORS policy
```

**Causa:** CORS no configurado correctamente.

**Soluciones:**

#### Solución 1: Configurar CORS en Django

```python
# Backend/config/settings.py
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← Debe estar arriba
    'django.middleware.common.CommonMiddleware',
    # ...
]

# Desarrollo
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
]

# Producción
CORS_ALLOWED_ORIGINS = [
    'https://tuapp.com',
]

# Permitir credentials (cookies, auth headers)
CORS_ALLOW_CREDENTIALS = True

# Headers personalizados
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-organization-subdomain',  # ← Importante!
]
```

---

### ❌ Problema 10: Super admin no puede acceder

**Error:**
```
403 Forbidden
```

**Causa:** Usuario no tiene `is_superuser=True`.

**Soluciones:**

#### Solución 1: Crear super admin

```bash
# Backend
python create_superuser.py
```

#### Solución 2: Convertir usuario existente en super admin

```python
# Backend - Django shell
from users.models import User

user = User.objects.get(username='admin')
user.is_superuser = True
user.is_staff = True
user.save()

print(f"✅ {user.username} es ahora super admin")
```

---

### 🔍 Herramientas de Diagnóstico

#### Script: Verificar estado del sistema

```python
# Backend/check_system.py
from tenants.models import Organization
from partners.models import Partner
from users.models import User

def check_system():
    print("=" * 60)
    print("DIAGNÓSTICO DEL SISTEMA MULTI-TENANT")
    print("=" * 60)
    
    # Organizaciones
    orgs = Organization.objects.all()
    print(f"\n📊 ORGANIZACIONES: {orgs.count()}")
    for org in orgs:
        partners_count = Partner.objects.all_organizations().filter(
            organization=org
        ).count()
        print(f"  • {org.name} ({org.subdomain}): {partners_count} socios")
    
    # Usuarios
    users = User.objects.all()
    print(f"\n👥 USUARIOS: {users.count()}")
    print(f"  • Super admins: {users.filter(is_superuser=True).count()}")
    print(f"  • Activos: {users.filter(is_active=True).count()}")
    
    # Partners sin organización
    partners_sin_org = Partner.objects.all_organizations().filter(
        organization__isnull=True
    ).count()
    if partners_sin_org > 0:
        print(f"\n⚠️  ADVERTENCIA: {partners_sin_org} partners sin organización")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    check_system()
```

---

### 📚 Comandos Útiles

```bash
# Verificar organizaciones
python check_org_data.py

# Verificar organización específica
python check_org_data.py sanjuan

# Crear super admin
python create_superuser.py

# Aplicar migraciones
python manage.py migrate

# Ver migraciones pendientes
python manage.py showmigrations

# Django shell
python manage.py shell

# Ejecutar servidor
python manage.py runserver

# Crear datos de prueba
python create_test_organizations.py
```

---

### ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] El middleware `TenantMiddleware` está en `settings.MIDDLEWARE`
- [ ] Los modelos heredan de `TenantModel`
- [ ] El header `X-Organization-Subdomain` se envía en las requests
- [ ] La organización existe y está activa
- [ ] El usuario tiene membresía en la organización
- [ ] Las migraciones están aplicadas
- [ ] CORS está configurado correctamente
- [ ] Los datos tienen `organization_id` asignado

---

## 🎉 CONCLUSIÓN

Este documento cubre la arquitectura completa del sistema multi-tenant de cooperativas agrícolas:

✅ **PASO 1** - Introducción y arquitectura general  
✅ **PASO 2** - Middleware y filtrado automático  
✅ **PASO 3** - Modelos y apps del sistema  
✅ **PASO 4** - Gestión de organizaciones  
✅ **PASO 5** - Ejemplos prácticos y casos de uso  
✅ **PASO 6** - Troubleshooting y solución de problemas  

### Características Principales:

- 🏢 **Multi-Tenant** - Múltiples cooperativas en una sola aplicación
- 🔒 **Aislamiento de Datos** - Cada cooperativa ve solo sus datos
- 🚀 **Escalable** - Agregar cooperativas es instantáneo
- 🛡️ **Seguro** - Validación de acceso en middleware
- 🔄 **Automático** - Filtrado transparente con TenantManager
- 💰 **SaaS** - Planes y límites por organización

### Modelo Implementado:

**Shared Database, Shared Schema**
- Una base de datos PostgreSQL (Neon)
- Un schema (`public`)
- Filtrado por `organization_id`
- Middleware + Manager automático

### Próximos Pasos:

1. Revisar este documento para entender la arquitectura
2. Usar los ejemplos prácticos como referencia
3. Consultar troubleshooting ante problemas
4. Extender el sistema según necesidades

---

**Documentación creada:** Noviembre 2024  
**Versión:** 1.0  
**Proyecto:** Sistema de Cooperativas Agrícolas Multi-Tenant
