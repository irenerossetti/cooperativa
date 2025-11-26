# Ejemplo: Migrar modelo Partner a Multi-Tenant

## 📝 Paso a paso para migrar un modelo existente

### Paso 1: Modificar el modelo

**Antes (partners/models.py):**
```python
from django.db import models

class Partner(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    partner_code = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # ... otros campos
```

**Después (partners/models.py):**
```python
from django.db import models
from tenants.managers import TenantModel  # Importar TenantModel

class Partner(TenantModel):  # Heredar de TenantModel en lugar de models.Model
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    partner_code = models.CharField(max_length=20)  # Quitar unique=True
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # ... otros campos
    
    class Meta:
        # Agregar unique_together para mantener unicidad por organización
        unique_together = [['organization', 'partner_code']]
```

### Paso 2: Crear la migración

```bash
python manage.py makemigrations partners
```

Esto creará una migración que:
- Agrega el campo `organization` (ForeignKey a Organization)
- Modifica las constraints de unicidad

### Paso 3: Asignar organización a datos existentes

Crea un script de migración de datos:

**migrate_partners_to_tenant.py:**
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from partners.models import Partner
from tenants.models import Organization

# Obtener o crear una organización por defecto
default_org, created = Organization.objects.get_or_create(
    subdomain='default',
    defaults={
        'name': 'Organización Principal',
        'email': 'admin@cooperativa.com',
        'plan': 'ENTERPRISE',
        'status': 'ACTIVE',
    }
)

print(f"Organización: {default_org.name}")

# Asignar todos los partners existentes a la organización por defecto
partners_updated = Partner.objects.filter(organization__isnull=True).update(
    organization=default_org
)

print(f"✅ {partners_updated} partners migrados a {default_org.name}")
```

### Paso 4: Aplicar la migración

```bash
python manage.py migrate partners
python migrate_partners_to_tenant.py
```

### Paso 5: Actualizar las vistas (si es necesario)

La mayoría de las vistas funcionarán automáticamente, pero puedes optimizarlas:

**Antes:**
```python
class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
```

**Después (opcional, ya funciona automáticamente):**
```python
class PartnerViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer
    
    def get_queryset(self):
        # El filtro por organización ya se aplica automáticamente
        # pero puedes agregar filtros adicionales
        return Partner.objects.all()
    
    def perform_create(self, serializer):
        # La organización se asigna automáticamente
        serializer.save()
```

## 🔄 Orden recomendado de migración

Migra los modelos en este orden para evitar problemas de dependencias:

1. **Modelos base** (sin dependencias):
   - Community
   - PaymentMethod
   - ProductCategory

2. **Modelos de usuarios**:
   - Partner (depende de User)
   - Role (depende de User)

3. **Modelos de inventario**:
   - Product
   - ProductVariant
   - Stock

4. **Modelos de operaciones**:
   - Campaign
   - Order
   - Payment
   - Shipment

5. **Modelos de reportes y auditoría**:
   - AuditLog
   - Report
   - Analytics

## ⚠️ Consideraciones importantes

### Campos unique

Los campos `unique=True` deben cambiarse a `unique_together` con organization:

```python
# Antes
email = models.EmailField(unique=True)

# Después
email = models.EmailField()

class Meta:
    unique_together = [['organization', 'email']]
```

### Relaciones entre modelos

Si un modelo tiene ForeignKey a otro modelo tenant:

```python
class Order(TenantModel):
    customer = models.ForeignKey(Partner, on_delete=models.CASCADE)
    # Ambos Order y Partner tienen organization
    # Django validará que pertenezcan a la misma organización
```

### Queries complejas

Para queries que cruzan organizaciones (solo admin):

```python
# Obtener todos los partners de todas las organizaciones
all_partners = Partner.objects.all_organizations()

# Filtrar por organización específica
org = Organization.objects.get(subdomain='sanjuan')
partners = Partner.objects.all_organizations().filter(organization=org)
```

## 🧪 Testing

Después de migrar, prueba:

1. **Crear registros**:
```bash
curl -X POST http://localhost:8000/api/partners/ \
  -H "X-Organization-Subdomain: sanjuan" \
  -H "Content-Type: application/json" \
  -d '{"partner_code": "P001", "status": "ACTIVE"}'
```

2. **Listar registros**:
```bash
curl http://localhost:8000/api/partners/?org=sanjuan
```

3. **Verificar aislamiento**:
```bash
# Crear en organización 1
curl -X POST http://localhost:8000/api/partners/?org=sanjuan \
  -d '{"partner_code": "P001"}'

# Intentar ver desde organización 2 (no debería aparecer)
curl http://localhost:8000/api/partners/?org=progreso
```

## 📊 Script completo de migración

**migrate_all_models.py:**
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from partners.models import Partner, Community
from inventory.models import Product
from sales.models import Order
# ... importar otros modelos

# Crear organización por defecto
default_org, _ = Organization.objects.get_or_create(
    subdomain='default',
    defaults={
        'name': 'Cooperativa Principal',
        'email': 'admin@cooperativa.com',
        'plan': 'ENTERPRISE',
        'status': 'ACTIVE',
        'max_users': 999,
        'max_products': 9999,
    }
)

print(f"Organización por defecto: {default_org.name}\n")

# Migrar cada modelo
models_to_migrate = [
    ('Community', Community),
    ('Partner', Partner),
    ('Product', Product),
    ('Order', Order),
    # ... agregar más modelos
]

for model_name, model_class in models_to_migrate:
    try:
        count = model_class.objects.filter(organization__isnull=True).update(
            organization=default_org
        )
        print(f"✅ {model_name}: {count} registros migrados")
    except Exception as e:
        print(f"❌ {model_name}: Error - {str(e)}")

print("\n🎉 Migración completada!")
```

## 🚀 Resultado final

Después de la migración:

- ✅ Todos los datos existentes pertenecen a una organización
- ✅ Nuevos registros se asignan automáticamente a la organización actual
- ✅ Los datos están aislados por organización
- ✅ Las APIs funcionan con multi-tenancy
- ✅ El sistema está listo para SaaS

## 📞 Soporte

Si encuentras problemas durante la migración:

1. Revisa los logs de Django
2. Verifica que el middleware esté activo
3. Confirma que la organización existe y está activa
4. Revisa la guía completa en `MULTI_TENANT_GUIDE.md`
