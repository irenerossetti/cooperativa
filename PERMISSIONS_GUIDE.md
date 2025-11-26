# Guía de Sistema de Permisos Granulares

## Configuración Inicial

### 1. Configurar permisos por defecto en los roles

```bash
cd Backend
python setup_default_permissions.py
```

Esto creará/actualizará los roles ADMIN, PARTNER, OPERATOR con permisos predefinidos.

## Uso en Frontend

### Importar el hook y componente

```javascript
import PermissionGuard from '../components/PermissionGuard';
import { usePermissions } from '../hooks/usePermissions';
```

### Ejemplo 1: Ocultar botón de eliminar

```javascript
<PermissionGuard permission="users.delete">
  <button onClick={handleDelete} className="text-red-600">
    <Trash2 className="w-4 h-4" />
  </button>
</PermissionGuard>
```

### Ejemplo 2: Ocultar botón de crear

```javascript
<PermissionGuard permission="users.create">
  <button onClick={() => setShowModal(true)}>
    <Plus className="w-4 h-4" /> Nuevo Usuario
  </button>
</PermissionGuard>
```

### Ejemplo 3: Usar el hook directamente

```javascript
const { hasPermission } = usePermissions();

const handleDelete = (id) => {
  if (!hasPermission('users.delete')) {
    alert('No tienes permisos para eliminar usuarios');
    return;
  }
  // Proceder con eliminación
};
```

### Ejemplo 4: Múltiples permisos (requiere todos)

```javascript
<PermissionGuard permissions={['users.view', 'users.edit']} requireAll>
  <button>Editar Usuario</button>
</PermissionGuard>
```

### Ejemplo 5: Múltiples permisos (requiere al menos uno)

```javascript
<PermissionGuard permissions={['users.view', 'users.edit']}>
  <div>Contenido visible si tiene view O edit</div>
</PermissionGuard>
```

## Uso en Backend

### Validar permisos en vistas

```python
from rest_framework.decorators import action
from rest_framework.response import Response

@action(detail=True, methods=['delete'])
def delete_user(self, request, pk=None):
    # Validar permiso
    if not request.user.has_permission('users.delete'):
        return Response(
            {'error': 'No tienes permisos para eliminar usuarios'},
            status=403
        )
    
    # Proceder con eliminación
    user = self.get_object()
    user.delete()
    return Response({'message': 'Usuario eliminado'})
```

## Estructura de Permisos

Los permisos se almacenan en formato JSON en el campo `permissions` del modelo Role:

```json
{
  "users": {
    "view": true,
    "create": true,
    "edit": true,
    "delete": false
  },
  "products": {
    "view": true,
    "create": false,
    "edit": false,
    "delete": false
  },
  "ui": {
    "show_delete_buttons": false,
    "show_prices": true,
    "show_costs": false
  }
}
```

## Permisos Predefinidos

### ADMIN
- Todos los permisos habilitados
- Puede ver, crear, editar y eliminar en todos los módulos

### PARTNER (Socio/Cliente)
- Solo puede ver productos y campañas
- Puede crear ventas
- No puede eliminar nada
- No ve costos

### OPERATOR (Operador)
- Puede ver, crear y editar (pero no eliminar)
- Ve precios y costos
- Puede exportar reportes

## Agregar Nuevos Permisos

Para agregar un nuevo permiso, simplemente edita el rol desde la interfaz de gestión de roles o actualiza el script `setup_default_permissions.py`.

No requiere cambios en la base de datos, solo actualizar el JSON del campo `permissions`.
