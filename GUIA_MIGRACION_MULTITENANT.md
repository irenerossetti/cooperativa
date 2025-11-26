# 🚀 Guía Completa: Migración a Multi-Tenant

## 📋 Resumen

Esta guía te llevará paso a paso para convertir tu sistema actual a multi-tenant, permitiendo que múltiples cooperativas usen la misma instancia con datos completamente aislados.

## ⚠️ IMPORTANTE: Antes de Empezar

1. **Haz backup de tu base de datos**
2. **Haz backup de tu código**
3. **Prueba en un entorno de desarrollo primero**
4. **Lee toda la guía antes de ejecutar comandos**

## 🎯 Objetivo

Convertir todos los modelos existentes para que:
- Hereden de `TenantModel` en lugar de `models.Model`
- Tengan un campo `organization` (ForeignKey)
- Se filtren automáticamente por organización
- Mantengan la unicidad por organización

## 📊 Estado Actual vs Estado Objetivo

### Estado Actual ❌
```python
class Partner(models.Model):
    ci = models.CharField(max_length=10, unique=True)
    # ... otros campos
```
- Los datos NO están aislados por organización
- Cualquier usuario puede ver datos de cualquier cooperativa
- No es un sistema SaaS real

### Estado Objetivo ✅
```python
class Partner(TenantModel):
    ci = models.CharField(max_length=10)
    # ... otros campos
    
    class Meta:
        unique_together = [['organization', 'ci']]
```
- Cada registro pertenece a una organización
- Los datos se filtran automáticamente
- Sistema SaaS funcional

---

## 🔧 PASO 1: Preparación

### 1.1 Verificar que el sistema multi-tenant está instalado

```bash
cd Backend
python manage.py shell
```

```python
from tenants.models import Organization
from tenants.managers import TenantModel
print("✅ Multi-tenant instalado correctamente")
exit()
```

### 1.2 Crear backup de la base de datos

**PostgreSQL:**
```bash
pg_dump -U usuario -d nombre_bd > backup_antes_migracion.sql
```

**SQLite (desarrollo):**
```bash
cp db.sqlite3 db.sqlite3.backup
```

### 1.3 Crear backup del código

```bash
git add .
git commit -m "Backup antes de migración multi-tenant"
git branch backup-pre-multitenant
```

---

## 🔧 PASO 2: Análisis de Modelos

### 2.1 Identificar modelos a migrar

```bash
python convert_models_to_tenant.py --dry-run
```

Este comando te mostrará:
- Qué modelos necesitan cambios
- Qué campos tienen `unique=True`
- Sugerencias de cambios

**Ejemplo de salida:**
```
📄 Procesando: Backend/partners/models.py
✅ Agregado import de TenantModel
✅ Convertida herencia a TenantModel
⚠️  Campos unique encontrados: ci, nit
  # TODO: Cambiar ci de unique=True a unique_together
  # En Meta: unique_together = [['organization', 'ci']]
```

### 2.2 Revisar la lista de modelos

Los siguientes modelos serán migrados:

**Sprint 1:**
- `partners.Community`
- `partners.Partner`
- `parcels.Parcel`
- `parcels.SoilType`
- `parcels.Crop`

**Sprint 2:**
- `campaigns.Campaign`
- `farm_activities.FarmActivity`
- `inventory.InventoryCategory`
- `inventory.InventoryItem`
- `inventory.InventoryMovement`
- `inventory.StockAlert`
- `production.HarvestedProduct`

**Sprint 3:**
- `sales.PaymentMethod`
- `sales.Customer`
- `sales.Order`
- `sales.OrderItem`
- `sales.Payment`
- `requests.PartnerRequest`
- `pricing.PriceList`
- `shipping.Shipment`

**Sprint 4:**
- `financial.ExpenseCategory`
- `financial.FieldExpense`
- `financial.ParcelProfitability`
- `reports.ReportType`
- `reports.GeneratedReport`
- `traceability.ParcelTraceability`
- `analytics.PriceTrend`
- `ai_recommendations.*` (todos los modelos)

**Sprint 5:**
- `monitoring.CropMonitoring`
- `monitoring.CropAlert`
- `weather.WeatherData`
- `weather.WeatherForecast`
- `weather.WeatherAlert`

**Auditoría:**
- `audit.AuditLog`

---

## 🔧 PASO 3: Modificar los Modelos

### Opción A: Automática (Recomendada)

```bash
# Ver cambios sin aplicar
python convert_models_to_tenant.py --dry-run

# Aplicar cambios (crea backups automáticamente)
python convert_models_to_tenant.py --apply
```

### Opción B: Manual (Para control total)

Para cada archivo `models.py`:

#### 3.1 Agregar import

```python
from tenants.managers import TenantModel
```

#### 3.2 Cambiar herencia

**Antes:**
```python
class Partner(models.Model):
```

**Después:**
```python
class Partner(TenantModel):
```

#### 3.3 Actualizar campos unique

**Antes:**
```python
ci = models.CharField(max_length=10, unique=True)
nit = models.CharField(max_length=15, unique=True)
```

**Después:**
```python
ci = models.CharField(max_length=10)  # Quitar unique=True
nit = models.CharField(max_length=15)  # Quitar unique=True

class Meta:
    unique_together = [
        ['organization', 'ci'],
        ['organization', 'nit'],
    ]
```

#### 3.4 Ejemplo completo

**Antes (partners/models.py):**
```python
from django.db import models
from users.models import User

class Partner(models.Model):
    ci = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    # ... otros campos
    
    class Meta:
        db_table = 'partners'
        ordering = ['-created_at']
```

**Después (partners/models.py):**
```python
from django.db import models
from users.models import User
from tenants.managers import TenantModel  # ← NUEVO

class Partner(TenantModel):  # ← CAMBIO
    ci = models.CharField(max_length=10)  # ← Sin unique=True
    first_name = models.CharField(max_length=100)
    # ... otros campos
    
    class Meta:
        db_table = 'partners'
        ordering = ['-created_at']
        unique_together = [['organization', 'ci']]  # ← NUEVO
```

---

## 🔧 PASO 4: Crear Migraciones

### 4.1 Generar migraciones

```bash
python manage.py makemigrations
```

Esto creará migraciones para agregar el campo `organization` a todos los modelos.

**Ejemplo de salida:**
```
Migrations for 'partners':
  partners/migrations/0002_add_organization.py
    - Add field organization to partner
    - Alter unique_together for partner
Migrations for 'campaigns':
  campaigns/migrations/0002_add_organization.py
    - Add field organization to campaign
...
```

### 4.2 Revisar las migraciones

Abre los archivos de migración generados y verifica que:
- Se agrega el campo `organization` como ForeignKey
- Se actualizan las constraints de unicidad
- No hay errores de sintaxis

### 4.3 Aplicar migraciones

```bash
python manage.py migrate
```

**⚠️ IMPORTANTE:** Esto agregará la columna `organization_id` a todas las tablas, pero los valores serán NULL inicialmente.

---

## 🔧 PASO 5: Migrar Datos Existentes

### 5.1 Ejecutar script de migración

```bash
python migrate_to_multitenant.py
```

Este script:
1. Crea una organización por defecto llamada "Cooperativa Principal"
2. Asigna el usuario admin como OWNER de esa organización
3. Asigna todos los datos existentes a esa organización

**Ejemplo de salida:**
```
🚀 MIGRACIÓN A MULTI-TENANT
======================================================================

📋 Paso 1: Identificando modelos a migrar...
----------------------------------------------------------------------
Encontrados 45 modelos que necesitan migración:
  - partners.Community (tabla: communities)
  - partners.Partner (tabla: partners)
  - campaigns.Campaign (tabla: campaigns)
  ...

📋 Paso 2: Creando organización por defecto...
----------------------------------------------------------------------
✅ Organización creada: Cooperativa Principal
✅ Usuario admin asignado como OWNER de Cooperativa Principal

📋 Paso 3: Migrando datos existentes...
----------------------------------------------------------------------
✅ Community: 3 registros migrados
✅ Partner: 15 registros migrados
✅ Campaign: 5 registros migrados
...

🎉 MIGRACIÓN COMPLETADA
======================================================================
Total de registros migrados: 250
Organización: Cooperativa Principal (subdomain: default)
```

### 5.2 Verificar la migración

```bash
python manage.py shell
```

```python
from partners.models import Partner
from tenants.models import Organization

# Verificar que todos los partners tienen organización
partners_sin_org = Partner.objects.all_organizations().filter(organization__isnull=True).count()
print(f"Partners sin organización: {partners_sin_org}")  # Debe ser 0

# Verificar la organización por defecto
org = Organization.objects.get(subdomain='default')
print(f"Organización: {org.name}")
print(f"Partners en esta org: {Partner.objects.filter(organization=org).count()}")
```

---

## 🔧 PASO 6: Probar el Sistema

### 6.1 Probar filtrado automático

```bash
python manage.py shell
```

```python
from partners.models import Partner
from tenants.middleware import set_current_organization
from tenants.models import Organization

# Obtener la organización
org = Organization.objects.get(subdomain='default')

# Establecer contexto
set_current_organization(org)

# Listar partners (debe filtrar automáticamente)
partners = Partner.objects.all()
print(f"Partners en contexto: {partners.count()}")

# Listar sin filtro (admin)
all_partners = Partner.objects.all_organizations()
print(f"Partners totales: {all_partners.count()}")
```

### 6.2 Probar API con query parameter

```bash
# Listar partners de la organización default
curl "http://localhost:8000/api/partners/partners/?org=default"

# Crear un partner
curl -X POST "http://localhost:8000/api/partners/partners/?org=default" \
  -H "Content-Type: application/json" \
  -d '{
    "ci": "12345678",
    "first_name": "Juan",
    "last_name": "Pérez",
    "community": 1
  }'
```

### 6.3 Crear organizaciones de prueba

```bash
python create_test_organizations.py
```

Esto crea:
- **sanjuan** - Cooperativa San Juan (PROFESSIONAL)
- **progreso** - Cooperativa El Progreso (BASIC)
- **demo** - Cooperativa Demo (FREE)

### 6.4 Probar aislamiento de datos

```bash
# Crear partner en organización sanjuan
curl -X POST "http://localhost:8000/api/partners/partners/?org=sanjuan" \
  -H "Content-Type: application/json" \
  -d '{"ci": "11111111", "first_name": "Pedro", "last_name": "López", "community": 1}'

# Intentar ver desde organización progreso (NO debe aparecer)
curl "http://localhost:8000/api/partners/partners/?org=progreso"

# Ver desde organización sanjuan (SÍ debe aparecer)
curl "http://localhost:8000/api/partners/partners/?org=sanjuan"
```

---

## 🔧 PASO 7: Actualizar Frontend (Opcional)

### 7.1 Agregar selector de organización

Si un usuario pertenece a múltiples organizaciones, necesitas un selector:

```javascript
// En AuthContext.jsx
const [currentOrganization, setCurrentOrganization] = useState(null);
const [userOrganizations, setUserOrganizations] = useState([]);

// Obtener organizaciones del usuario
const fetchUserOrganizations = async () => {
  const response = await api.get('/tenants/my-organizations/');
  setUserOrganizations(response.data);
  if (response.data.length > 0) {
    setCurrentOrganization(response.data[0]);
  }
};
```

### 7.2 Incluir organización en requests

```javascript
// En api.js
api.interceptors.request.use((config) => {
  const org = localStorage.getItem('currentOrganization');
  if (org) {
    config.params = {
      ...config.params,
      org: org
    };
  }
  return config;
});
```

---

## ✅ PASO 8: Verificación Final

### Checklist de Verificación

- [ ] Todos los modelos heredan de `TenantModel`
- [ ] Todas las migraciones se aplicaron correctamente
- [ ] Todos los datos tienen `organization_id` asignado
- [ ] El filtrado automático funciona
- [ ] Las APIs responden correctamente con `?org=`
- [ ] Se pueden crear nuevas organizaciones
- [ ] Los datos están aislados entre organizaciones
- [ ] El usuario admin es OWNER de la organización default
- [ ] Los tests pasan correctamente

### Comandos de Verificación

```bash
# 1. Verificar migraciones
python manage.py showmigrations

# 2. Verificar datos
python manage.py shell
>>> from tenants.models import Organization
>>> Organization.objects.count()  # Debe ser > 0
>>> from partners.models import Partner
>>> Partner.objects.all_organizations().filter(organization__isnull=True).count()  # Debe ser 0

# 3. Verificar API
curl "http://localhost:8000/api/partners/partners/?org=default"
```

---

## 🐛 Solución de Problemas

### Problema 1: "No se puede guardar sin una organización"

**Causa:** El middleware no está detectando la organización.

**Solución:**
```python
# Verificar que el middleware está en settings.py
MIDDLEWARE = [
    # ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'tenants.middleware.TenantMiddleware',  # ← Debe estar aquí
    # ...
]
```

### Problema 2: "Columna organization_id no existe"

**Causa:** No se ejecutaron las migraciones.

**Solución:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Problema 3: "IntegrityError: NOT NULL constraint failed"

**Causa:** Hay datos sin organización asignada.

**Solución:**
```bash
python migrate_to_multitenant.py
```

### Problema 4: "Los datos no se filtran por organización"

**Causa:** El modelo no hereda de `TenantModel`.

**Solución:**
Verificar que el modelo hereda de `TenantModel` y no de `models.Model`.

### Problema 5: "unique constraint failed"

**Causa:** Campos unique no se actualizaron a unique_together.

**Solución:**
Cambiar `unique=True` a `unique_together = [['organization', 'campo']]` en Meta.

---

## 📊 Resumen de Archivos Modificados

### Archivos Creados
- `Backend/migrate_to_multitenant.py` - Script de migración de datos
- `Backend/convert_models_to_tenant.py` - Script de conversión de modelos
- `Backend/GUIA_MIGRACION_MULTITENANT.md` - Esta guía

### Archivos Modificados
- `Backend/*/models.py` - Todos los modelos de negocio
- `Backend/*/migrations/` - Nuevas migraciones

### Archivos de Backup
- `Backend/*/models.py.backup` - Backups automáticos
- `db.sqlite3.backup` - Backup de base de datos

---

## 🎯 Próximos Pasos

Después de completar la migración:

1. **Crear landing page** para registro público de cooperativas
2. **Implementar sistema de pagos** (Stripe/PayPal)
3. **Agregar límites por plan** (validar max_users, max_products)
4. **Dashboard de administración** para gestionar organizaciones
5. **Métricas por organización** (uso, facturación, etc.)
6. **Onboarding mejorado** para nuevas cooperativas

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa esta guía completa
2. Consulta `MULTI_TENANT_GUIDE.md`
3. Revisa `EJEMPLO_MIGRACION_TENANT.md`
4. Verifica los logs de Django
5. Restaura desde backup si es necesario

---

## 🎉 ¡Felicidades!

Si completaste todos los pasos, tu sistema ahora es un **SaaS multi-tenant funcional** que puede soportar múltiples cooperativas con datos completamente aislados.

**Beneficios logrados:**
- ✅ Aislamiento completo de datos
- ✅ Escalabilidad horizontal
- ✅ Modelo de negocio SaaS
- ✅ Gestión centralizada
- ✅ Actualizaciones para todos los tenants
- ✅ Métricas agregadas

**¡Tu sistema está listo para crecer!** 🚀
