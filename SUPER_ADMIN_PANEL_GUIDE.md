# 🛡️ Panel de Super Admin - Guía Completa

## 📋 Descripción

El Panel de Super Admin es una interfaz de administración centralizada para gestionar todas las cooperativas (organizaciones) del sistema SaaS multi-tenant.

## 🎯 Características Principales

### 1. Dashboard con Estadísticas Globales
- Total de organizaciones registradas
- Organizaciones activas, en prueba, suspendidas
- Total de usuarios en el sistema
- Nuevas organizaciones del mes
- Distribución por planes

### 2. Gestión de Organizaciones
- **Listar** todas las organizaciones con filtros
- **Ver detalles** completos de cada organización
- **Crear** nuevas organizaciones
- **Editar** información, planes y límites
- **Activar/Suspender** organizaciones
- **Desactivar** (soft delete) organizaciones

### 3. Filtros y Búsqueda
- Búsqueda por nombre, subdominio o email
- Filtro por estado (Activo, Prueba, Suspendido, Cancelado)
- Filtro por plan (Gratuito, Básico, Profesional, Enterprise)

### 4. Información Detallada
Para cada organización puedes ver:
- Información básica (nombre, subdominio, contacto)
- Plan y estado actual
- Límites (usuarios, productos, almacenamiento)
- Lista de miembros con sus roles
- Fechas de creación y vencimiento

## 🚀 Acceso al Panel

### Desde el Landing Page
1. Ve a la página principal: `http://localhost:5173/`
2. Haz clic en el botón **"Admin"** (con icono de escudo) en la barra de navegación
3. Serás redirigido a `/super-admin`

### URL Directa
Accede directamente a: `http://localhost:5173/super-admin`

## 🔐 Credenciales de Acceso

### Crear Super Usuario

Ejecuta el script para crear un super usuario:

```bash
cd Backend
python create_superuser.py
```

**Credenciales por defecto:**
- Username: `superadmin`
- Password: `admin123`
- Email: `superadmin@agrocooperativa.com`

⚠️ **IMPORTANTE:** Cambia estas credenciales en producción.

### Requisitos de Acceso
- Solo usuarios con `is_superuser=True` pueden acceder
- Si un usuario normal intenta acceder, será redirigido
- Todas las acciones son registradas en el sistema de auditoría

## 📡 Endpoints del Backend

### Estadísticas del Dashboard
```
GET /api/tenants/super-admin/stats/
```

Respuesta:
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
    "total": 150,
    "active": 142
  },
  "plan_distribution": {
    "FREE": 3,
    "BASIC": 4,
    "PROFESSIONAL": 2,
    "ENTERPRISE": 1
  },
  "recent_organizations": [...]
}
```

### Listar Organizaciones
```
GET /api/tenants/super-admin/organizations/
GET /api/tenants/super-admin/organizations/?search=cooperativa
GET /api/tenants/super-admin/organizations/?status=ACTIVE
GET /api/tenants/super-admin/organizations/?plan=PROFESSIONAL
```

### Ver Detalle de Organización
```
GET /api/tenants/super-admin/organizations/{id}/
```

### Crear Organización
```
POST /api/tenants/super-admin/organizations/create/
Content-Type: application/json

{
  "organization_name": "Cooperativa Nueva",
  "subdomain": "nueva",
  "email": "contacto@nueva.com",
  "plan": "PROFESSIONAL",
  "admin_username": "admin_nueva",
  "admin_email": "admin@nueva.com",
  "admin_password": "password123"
}
```

### Actualizar Organización
```
PUT /api/tenants/super-admin/organizations/{id}/update/
Content-Type: application/json

{
  "plan": "ENTERPRISE",
  "status": "ACTIVE",
  "max_users": 100,
  "max_products": 1000
}
```

### Desactivar Organización
```
DELETE /api/tenants/super-admin/organizations/{id}/delete/
```

## 🎨 Interfaz de Usuario

### Colores y Diseño
- **Tema oscuro** (gray-900, gray-800) para reducir fatiga visual
- **Rojo** para elementos de super admin (distintivo y de alerta)
- **Badges de estado:**
  - Verde: Activo
  - Azul: Prueba
  - Amarillo: Suspendido
  - Rojo: Cancelado

### Acciones Rápidas
Desde la tabla de organizaciones:
- 👁️ **Ver detalles** - Abre modal con información completa
- ✅ **Activar** - Cambia estado a ACTIVE (solo si está suspendida)
- ⚠️ **Suspender** - Cambia estado a SUSPENDED (solo si está activa)
- 🗑️ **Desactivar** - Soft delete (cambia a CANCELLED)

## 🔒 Seguridad

### Permisos
- Solo usuarios con `is_superuser=True` pueden acceder
- Implementado con `IsSuperAdmin` permission class
- Verificación en frontend y backend

### Auditoría
- Todas las acciones del super admin son registradas
- Se guarda: usuario, acción, timestamp, datos modificados
- Accesible desde el sistema de auditoría

### Mejores Prácticas
1. **Nunca compartas** las credenciales de super admin
2. **Cambia la contraseña** regularmente
3. **Revisa los logs** de auditoría periódicamente
4. **Usa 2FA** en producción (implementar)
5. **Limita el acceso** solo a personal autorizado

## 📊 Casos de Uso

### 1. Onboarding de Nueva Cooperativa
1. Cliente se registra desde el landing
2. Super admin revisa la solicitud
3. Activa la organización y asigna plan
4. Configura límites según el plan contratado

### 2. Gestión de Planes
1. Cliente solicita upgrade de plan
2. Super admin actualiza el plan
3. Ajusta límites (usuarios, productos, storage)
4. Cliente recibe acceso inmediato a nuevas funcionalidades

### 3. Soporte Técnico
1. Cliente reporta problema
2. Super admin accede a detalles de la organización
3. Revisa miembros, configuración y estado
4. Realiza ajustes necesarios

### 4. Suspensión por Falta de Pago
1. Sistema detecta pago vencido
2. Super admin suspende la organización
3. Cliente no puede acceder hasta regularizar
4. Al pagar, super admin reactiva la cuenta

### 5. Análisis de Crecimiento
1. Super admin revisa estadísticas globales
2. Identifica tendencias de crecimiento
3. Analiza distribución de planes
4. Toma decisiones de negocio

## 🛠️ Desarrollo y Personalización

### Agregar Nuevas Estadísticas
Edita `Backend/tenants/views.py` en `super_admin_dashboard_stats`:

```python
# Agregar nueva métrica
total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total']

return Response({
    # ... estadísticas existentes
    'sales': {
        'total': total_sales
    }
})
```

### Agregar Nuevos Filtros
Edita `Backend/tenants/views.py` en `super_admin_list_organizations`:

```python
# Agregar filtro por fecha
created_after = request.GET.get('created_after')
if created_after:
    queryset = queryset.filter(created_at__gte=created_after)
```

### Personalizar UI
Edita `Frontend/src/pages/dashboards/SuperAdminDashboard.jsx`:

```jsx
// Agregar nueva tarjeta de estadística
<div className="bg-gray-800 rounded-xl p-6">
  <h3 className="text-2xl font-bold text-white">
    {stats.nueva_metrica}
  </h3>
  <p className="text-gray-400">Nueva Métrica</p>
</div>
```

## 🧪 Testing

### Probar el Panel

1. **Crear super usuario:**
```bash
cd Backend
python create_superuser.py
```

2. **Crear organizaciones de prueba:**
```bash
python create_test_organizations.py
```

3. **Acceder al panel:**
- Ve a `http://localhost:5173/super-admin`
- Login con `superadmin` / `admin123`
- Explora las funcionalidades

### Verificar Permisos

```bash
# Intentar acceder con usuario normal (debe fallar)
curl -X GET http://localhost:8000/api/tenants/super-admin/stats/ \
  -H "Cookie: sessionid=<session_normal_user>"

# Acceder con super admin (debe funcionar)
curl -X GET http://localhost:8000/api/tenants/super-admin/stats/ \
  -H "Cookie: sessionid=<session_superuser>"
```

## 📝 Notas Adicionales

### Diferencias con Django Admin
- **Django Admin:** Panel técnico para desarrolladores
- **Super Admin Panel:** Interfaz de negocio para gestión de cooperativas
- Ambos pueden coexistir y tienen propósitos diferentes

### Escalabilidad
- Diseñado para manejar cientos de organizaciones
- Paginación implementada en backend
- Filtros optimizados con índices de base de datos

### Futuras Mejoras
- [ ] Exportar lista de organizaciones a CSV/Excel
- [ ] Gráficos de crecimiento temporal
- [ ] Notificaciones automáticas (vencimientos, límites)
- [ ] Logs de actividad del super admin
- [ ] Autenticación de dos factores (2FA)
- [ ] Gestión de facturación integrada
- [ ] Chat de soporte integrado

## 🆘 Troubleshooting

### Error: "Acceso denegado"
- Verifica que el usuario tenga `is_superuser=True`
- Ejecuta: `python create_superuser.py`

### No se cargan las organizaciones
- Verifica que el backend esté corriendo
- Revisa la consola del navegador para errores
- Verifica la conexión a la base de datos

### Error 403 en endpoints
- Verifica que estés autenticado como super admin
- Revisa que la sesión no haya expirado
- Limpia cookies y vuelve a hacer login

## 📞 Soporte

Para problemas o preguntas sobre el Panel de Super Admin:
1. Revisa esta documentación
2. Consulta los logs del backend
3. Revisa el sistema de auditoría
4. Contacta al equipo de desarrollo

---

**Última actualización:** Noviembre 2024
**Versión:** 1.0.0
