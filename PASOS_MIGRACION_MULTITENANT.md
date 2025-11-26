# 🚀 Pasos para Migrar a Multi-Tenant

## ⚡ Inicio Rápido (5 pasos)

### 📋 Pre-requisitos
- ✅ Backup de base de datos
- ✅ Backup de código (git commit)
- ✅ Entorno de desarrollo activo

---

## PASO 1: Verificar Estado Actual

```bash
cd Backend
python verify_multitenant.py
```

Esto te mostrará qué modelos necesitan migración.

---

## PASO 2: Convertir Modelos Automáticamente

```bash
# Ver qué cambios se harán (sin aplicar)
python convert_models_to_tenant.py --dry-run

# Aplicar cambios (crea backups automáticos)
python convert_models_to_tenant.py --apply
```

**Esto modificará todos los archivos `models.py` para:**
- Importar `TenantModel`
- Cambiar herencia de `models.Model` a `TenantModel`
- Identificar campos `unique=True` que necesitan ajuste manual

---

## PASO 3: Ajustar Campos Unique Manualmente

Busca en los archivos modificados los comentarios `# TODO` y actualiza:

**Ejemplo en `partners/models.py`:**

```python
# Cambiar esto:
ci = models.CharField(max_length=10, unique=True)

# Por esto:
ci = models.CharField(max_length=10)

class Meta:
    unique_together = [['organization', 'ci']]
```

**Modelos con campos unique que debes revisar:**
- `partners.Partner` → ci, nit
- `campaigns.Campaign` → code
- `inventory.InventoryItem` → code
- `sales.Order` → order_number
- `parcels.Parcel` → code

---

## PASO 4: Crear y Aplicar Migraciones

```bash
# Generar migraciones
python manage.py makemigrations

# Revisar las migraciones generadas
# Verificar que se agrega el campo organization

# Aplicar migraciones
python manage.py migrate
```

---

## PASO 5: Migrar Datos Existentes

```bash
python migrate_to_multitenant.py
```

**Esto hará:**
1. Crear organización "Cooperativa Principal" (subdomain: default)
2. Asignar usuario admin como OWNER
3. Asignar todos los datos existentes a esa organización

---

## ✅ Verificación Final

```bash
python verify_multitenant.py
```

Debe mostrar: **"🎉 ¡Sistema multi-tenant completamente funcional!"**

---

## 🧪 Probar el Sistema

### 1. Crear organizaciones de prueba

```bash
python create_test_organizations.py
```

Crea 3 organizaciones:
- **default** - Cooperativa Principal
- **sanjuan** - Cooperativa San Juan
- **progreso** - Cooperativa El Progreso

### 2. Probar API con filtrado

```bash
# Listar partners de la organización default
curl "http://localhost:8000/api/partners/partners/?org=default"

# Listar partners de sanjuan
curl "http://localhost:8000/api/partners/partners/?org=sanjuan"
```

### 3. Probar aislamiento de datos

```bash
# Crear partner en sanjuan
curl -X POST "http://localhost:8000/api/partners/partners/?org=sanjuan" \
  -H "Content-Type: application/json" \
  -d '{
    "ci": "11111111",
    "first_name": "Pedro",
    "last_name": "López",
    "phone": "+59170000000",
    "community": 1
  }'

# Verificar que NO aparece en progreso
curl "http://localhost:8000/api/partners/partners/?org=progreso"

# Verificar que SÍ aparece en sanjuan
curl "http://localhost:8000/api/partners/partners/?org=sanjuan"
```

---

## 📊 Resumen de Archivos

### Creados
- ✅ `migrate_to_multitenant.py` - Migra datos existentes
- ✅ `convert_models_to_tenant.py` - Convierte modelos automáticamente
- ✅ `verify_multitenant.py` - Verifica el sistema
- ✅ `GUIA_MIGRACION_MULTITENANT.md` - Guía completa detallada
- ✅ `PASOS_MIGRACION_MULTITENANT.md` - Este archivo

### Modificados (después de ejecutar scripts)
- 📝 `*/models.py` - Todos los modelos de negocio
- 📝 `*/migrations/` - Nuevas migraciones

### Backups automáticos
- 💾 `*/models.py.backup` - Backups de modelos originales

---

## 🐛 Solución Rápida de Problemas

### Error: "No se puede guardar sin una organización"
```bash
# Verificar middleware en settings.py
# Debe estar después de AuthenticationMiddleware
```

### Error: "Columna organization_id no existe"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error: "IntegrityError: NOT NULL constraint"
```bash
python migrate_to_multitenant.py
```

### Los datos no se filtran
```python
# Verificar que el modelo hereda de TenantModel
class MiModelo(TenantModel):  # ← Correcto
    pass
```

---

## 📚 Documentación Completa

Para más detalles, consulta:
- `GUIA_MIGRACION_MULTITENANT.md` - Guía paso a paso detallada
- `MULTI_TENANT_GUIDE.md` - Guía de uso del sistema
- `EJEMPLO_MIGRACION_TENANT.md` - Ejemplos específicos

---

## 🎯 Tiempo Estimado

- **Paso 1-2:** 5 minutos
- **Paso 3:** 15-30 minutos (ajustes manuales)
- **Paso 4:** 5 minutos
- **Paso 5:** 5 minutos
- **Verificación:** 5 minutos

**Total: ~45 minutos**

---

## ✨ Resultado Final

Después de completar estos pasos tendrás:

✅ Sistema SaaS multi-tenant funcional
✅ Datos aislados por organización
✅ Filtrado automático en todas las queries
✅ API lista para múltiples cooperativas
✅ Base para modelo de negocio SaaS

---

## 🚀 ¡Comienza Ahora!

```bash
cd Backend
python verify_multitenant.py
```

¡Sigue los pasos y en menos de 1 hora tendrás tu sistema multi-tenant funcionando! 🎉
