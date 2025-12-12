# 🔧 Fix: ImportError TenantModel

## 🐛 Error
```
ImportError: cannot import name 'TenantModel' from 'tenants.models'
```

## 🔍 Causa
Los nuevos modelos estaban importando `TenantModel` desde `tenants.models` cuando debería ser desde `tenants.managers`.

## ✅ Solución Aplicada

### Archivos Corregidos:

#### 1. notifications/models.py
```python
# Antes:
from tenants.models import TenantModel

# Después:
from tenants.managers import TenantModel
```

#### 2. events/models.py
```python
# Antes:
from tenants.models import TenantModel

# Después:
from tenants.managers import TenantModel
```

#### 3. goals/models.py
```python
# Antes:
from tenants.models import TenantModel

# Después:
from tenants.managers import TenantModel
```

#### 4. qr_codes/models.py
```python
# Antes:
from tenants.models import TenantModel

# Después:
from tenants.managers import TenantModel
```

#### 5. ai_chat/models.py
```python
# Antes:
from tenants.models import TenantModel

# Después:
from tenants.managers import TenantModel
```

## 📝 Import Correcto

Para cualquier modelo que necesite multi-tenancy:

```python
from django.db import models
from tenants.managers import TenantModel  # ✅ Correcto

class MiModelo(TenantModel):
    # ... campos del modelo
    pass
```

## 🚀 Verificar

```bash
cd cooperativa
python manage.py check
python manage.py runserver
```

Debería iniciar sin errores.

## ✅ Estado
- [x] notifications/models.py corregido
- [x] events/models.py corregido
- [x] goals/models.py corregido
- [x] qr_codes/models.py corregido
- [x] ai_chat/models.py corregido

---

**Error resuelto** ✅
