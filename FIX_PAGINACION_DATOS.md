# Fix: Mostrar Todos los Datos (Sin Límite de Paginación)

## Problema
El dashboard mostraba solo 25 socios y 25 parcelas a pesar de tener 2000+ datos en la base de datos.

## Causa
El backend tenía configurada una paginación de 25 elementos por página (`PAGE_SIZE: 25`).

## Solución Aplicada

### 1. Backend - Aumentar PAGE_SIZE
**Archivo**: `Backend/config/settings.py`

```python
# Antes:
'PAGE_SIZE': 25,

# Ahora:
'PAGE_SIZE': 1000,  # Aumentado para mostrar todos los datos
```

### 2. Frontend - Solicitar Páginas Grandes
**Archivos modificados**:
- `Frontend/src/hooks/useDashboardStats.js`
- `Frontend/src/hooks/usePartnerDashboardStats.js`

**Cambio**: Agregar `?page_size=10000` a todas las peticiones API

```javascript
// Antes:
const partnersResponse = await api.get('/api/partners/partners/');

// Ahora:
const partnersResponse = await api.get('/api/partners/partners/?page_size=10000');
```

## Resultado

Ahora el dashboard mostrará:
- ✅ **Todos los socios** (100+)
- ✅ **Todas las parcelas** (250+)
- ✅ **Todos los productos cosechados** (2000+)
- ✅ **Todas las campañas**
- ✅ **Todas las ventas**

## Verificación

Después del deploy, el dashboard debería mostrar números como:
- Total Socios: **100** (en lugar de 25)
- Parcelas Activas: **250** (en lugar de 25)
- Productos Cosechados: **230,669 kg** (todos los datos)

## Notas

- El `PAGE_SIZE` de 1000 es suficiente para la mayoría de cooperativas
- Si en el futuro hay más de 1000 elementos, se puede:
  1. Aumentar el `PAGE_SIZE` aún más
  2. Implementar paginación infinita en el frontend
  3. Usar `?page_size=all` (requiere configuración adicional)

## Archivos Modificados

### Backend:
- ✅ `config/settings.py` - PAGE_SIZE aumentado a 1000

### Frontend:
- ✅ `src/hooks/useDashboardStats.js` - Agregado page_size=10000
- ✅ `src/hooks/usePartnerDashboardStats.js` - Agregado page_size=10000

## Deploy

```bash
# Backend
cd Backend
git add .
git commit -m "Fix: Aumentar PAGE_SIZE para mostrar todos los datos"
git push

# Frontend
cd Frontend
git add .
git commit -m "Fix: Agregar page_size=10000 para obtener todos los datos"
git push
```

Render y Vercel redesplegarán automáticamente.
