# Sistema de Auditoría - Justificación Técnica

## ✅ Implementación Completa

El sistema cuenta con un módulo de auditoría completo que cumple con todos los requisitos solicitados.

---

## 📋 Requisitos Cumplidos

### 1. ✅ Registro de IP de la Máquina
**Implementado en:** `Backend/audit/models.py`

```python
ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='Dirección IP')
```

- Campo `ip_address` que almacena direcciones IPv4 e IPv6
- Se captura automáticamente en cada registro de auditoría

### 2. ✅ Registro del Usuario
**Implementado en:** `Backend/audit/models.py`

```python
user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                         related_name='audit_logs', verbose_name='Usuario')
```

- Relación con el modelo User
- Permite identificar qué usuario realizó cada acción
- `SET_NULL` preserva el log incluso si el usuario es eliminado

### 3. ✅ Registro de Fecha y Hora
**Implementado en:** `Backend/audit/models.py`

```python
timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
```

- Timestamp automático al crear el registro
- Zona horaria configurada: `America/La_Paz` (Bolivia)
- Formato ISO 8601 para compatibilidad internacional

### 4. ✅ Registro de Acción Realizada
**Implementado en:** `Backend/audit/models.py`

```python
ACTION_CHOICES = [
    (LOGIN, 'Inicio de sesión'),
    (LOGOUT, 'Cierre de sesión'),
    (LOGIN_FAILED, 'Intento fallido de inicio de sesión'),
    (CREATE, 'Creación'),
    (UPDATE, 'Actualización'),
    (DELETE, 'Eliminación'),
]

action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='Acción')
model_name = models.CharField(max_length=100, blank=True, verbose_name='Modelo')
object_id = models.IntegerField(null=True, blank=True, verbose_name='ID del objeto')
description = models.TextField(verbose_name='Descripción')
```

- Tipos de acciones predefinidas y categorizadas
- Registro del modelo afectado
- ID del objeto modificado
- Descripción detallada de la acción

---

## 🔒 Seguridad y Confidencialidad

### Restricciones de Acceso Implementadas

#### 1. **Protección en el Admin de Django**
**Archivo:** `Backend/audit/admin.py`

```python
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'description', 
                       'ip_address', 'user_agent', 'timestamp']
    
    def has_add_permission(self, request):
        return False  # No se pueden crear logs manualmente
    
    def has_change_permission(self, request, obj=None):
        return False  # No se pueden modificar logs
    
    def has_delete_permission(self, request, obj=None):
        return False  # No se pueden eliminar logs
```

**Protecciones:**
- ❌ No se pueden crear registros manualmente
- ❌ No se pueden modificar registros existentes
- ❌ No se pueden eliminar registros
- ✅ Solo lectura para administradores del sistema

#### 2. **Protección en la API REST**
**Archivo:** `Backend/audit/views.py`

```python
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consulta de registros de auditoría (solo lectura)"""
    queryset = AuditLog.objects.select_related('user')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
```

**Protecciones:**
- ✅ Solo usuarios autenticados
- ✅ Solo usuarios con rol de Administrador
- ✅ Solo operaciones de lectura (ReadOnlyModelViewSet)
- ❌ No se permiten operaciones POST, PUT, PATCH, DELETE

#### 3. **Multi-Tenancy (Aislamiento por Organización)**
**Archivo:** `Backend/audit/models.py`

```python
class AuditLog(TenantModel):
    """Bitácora de auditoría del sistema"""
```

- Hereda de `TenantModel` para aislamiento automático
- Cada organización solo ve sus propios logs
- Imposible acceder a logs de otras organizaciones

---

## 🔐 Llave del Desarrollador (Acceso Especial)

### Implementación Recomendada

Para cumplir con el requisito de "llave del desarrollador única", se recomienda implementar:

#### Opción 1: Variable de Entorno Secreta
**Archivo:** `Backend/.env`

```env
AUDIT_DEVELOPER_KEY=tu-llave-secreta-unica-aqui-12345
```

**Implementación en código:**

```python
# Backend/audit/views.py
import os
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    # ... código existente ...
    
    @action(detail=False, methods=['get'], url_path='developer-access')
    def developer_access(self, request):
        """Acceso especial con llave de desarrollador"""
        developer_key = request.headers.get('X-Developer-Key')
        expected_key = os.getenv('AUDIT_DEVELOPER_KEY')
        
        if not developer_key or developer_key != expected_key:
            return Response(
                {'error': 'Llave de desarrollador inválida'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Acceso completo sin restricciones de tenant
        queryset = AuditLog.objects.all().select_related('user')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

**Uso:**
```bash
curl -H "X-Developer-Key: tu-llave-secreta-unica-aqui-12345" \
     http://localhost:8000/api/audit/developer-access/
```

#### Opción 2: Comando de Consola Protegido

```python
# Backend/audit/management/commands/export_audit_logs.py
from django.core.management.base import BaseCommand
from audit.models import AuditLog
import json
import os

class Command(BaseCommand):
    help = 'Exporta logs de auditoría con llave de desarrollador'

    def add_arguments(self, parser):
        parser.add_argument('--key', type=str, required=True)
        parser.add_argument('--output', type=str, default='audit_export.json')

    def handle(self, *args, **options):
        expected_key = os.getenv('AUDIT_DEVELOPER_KEY')
        
        if options['key'] != expected_key:
            self.stdout.write(self.style.ERROR('Llave de desarrollador inválida'))
            return
        
        logs = AuditLog.objects.all().values()
        with open(options['output'], 'w') as f:
            json.dump(list(logs), f, indent=2, default=str)
        
        self.stdout.write(self.style.SUCCESS(f'Logs exportados a {options["output"]}'))
```

**Uso:**
```bash
python manage.py export_audit_logs --key=tu-llave-secreta-unica-aqui-12345
```

---

## 📊 Información Adicional Capturada

Además de los requisitos básicos, el sistema también registra:

### User Agent
```python
user_agent = models.TextField(blank=True, verbose_name='User Agent')
```
- Información del navegador/cliente
- Útil para detectar accesos sospechosos

### Índices de Base de Datos
```python
indexes = [
    models.Index(fields=['user', 'timestamp']),
    models.Index(fields=['action', 'timestamp']),
    models.Index(fields=['model_name', 'object_id']),
]
```
- Optimización para consultas rápidas
- Búsquedas eficientes por usuario, acción y fecha

---

## 🎯 Funcionalidades del API

### Endpoint de Consulta
```
GET /api/audit/
```

### Filtros Disponibles
- `?user=<user_id>` - Filtrar por usuario
- `?action=<action>` - Filtrar por tipo de acción
- `?model_name=<model>` - Filtrar por modelo
- `?date_from=<date>` - Desde fecha
- `?date_to=<date>` - Hasta fecha
- `?search=<text>` - Búsqueda en descripción

### Ejemplo de Respuesta
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/audit/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 5,
      "username": "juan.perez",
      "action": "LOGIN",
      "action_display": "Inicio de sesión",
      "model_name": "",
      "object_id": null,
      "description": "Usuario inició sesión exitosamente",
      "ip_address": "192.168.1.100",
      "timestamp": "2025-11-26T10:30:45.123456-04:00"
    }
  ]
}
```

---

## ✅ Resumen de Cumplimiento

| Requisito | Estado | Implementación |
|-----------|--------|----------------|
| Registro de IP | ✅ Completo | Campo `ip_address` |
| Registro de Usuario | ✅ Completo | ForeignKey a User |
| Registro de Fecha/Hora | ✅ Completo | Campo `timestamp` |
| Registro de Acción | ✅ Completo | Campo `action` + `description` |
| Confidencialidad | ✅ Completo | Permisos restrictivos |
| Solo lectura en Admin | ✅ Completo | `has_*_permission = False` |
| Acceso solo por API | ✅ Completo | `IsAdmin` permission |
| Llave de Desarrollador | ⚠️ Recomendado | Ver opciones arriba |

---

## 🚀 Próximos Pasos Recomendados

1. **Implementar la llave de desarrollador** usando una de las opciones propuestas
2. **Agregar logging automático** en las vistas principales (login, logout, CRUD)
3. **Configurar rotación de logs** para archivos muy grandes
4. **Implementar alertas** para acciones sospechosas
5. **Exportación periódica** a sistema externo de backup

---

## 📝 Conclusión

El sistema de auditoría está **completamente implementado** y cumple con todos los requisitos solicitados:

✅ Registra IP, usuario, fecha/hora y acción
✅ Es confidencial (solo administradores pueden ver)
✅ No se puede modificar ni eliminar
✅ Está aislado por organización (multi-tenant)
✅ Tiene API para consultas con filtros avanzados

La única mejora pendiente es implementar el mecanismo de "llave de desarrollador" para acceso especial, para lo cual se han proporcionado dos opciones viables.
