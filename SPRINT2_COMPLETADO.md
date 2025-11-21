# Sprint 2 - Completado ✅

## Resumen de Implementación

Se ha implementado exitosamente el backend completo del Sprint 2 con Django REST Framework, cumpliendo con todas las historias de usuario y casos de uso.

## Nuevas Apps Creadas

```
Backend/
├── campaigns/          # Gestión de campañas agrícolas
│   ├── models.py       # Campaign
│   ├── views.py        # CRUD + acciones especiales
│   ├── serializers.py  # Validaciones
│   └── signals.py      # Auditoría automática
│
├── farm_activities/    # Labores agrícolas
│   ├── models.py       # FarmActivity, ActivityType
│   ├── views.py        # CRUD + reportes
│   ├── serializers.py  # Validaciones
│   └── signals.py      # Auditoría automática
│
├── inventory/          # Gestión de inventario
│   ├── models.py       # InventoryItem, InventoryMovement, StockAlert
│   ├── views.py        # CRUD + alertas + disponibilidad
│   ├── serializers.py  # Validaciones de stock
│   └── signals.py      # Alertas automáticas
│
└── production/         # Gestión de producción
    ├── models.py       # HarvestedProduct
    ├── views.py        # CRUD + reportes
    ├── serializers.py  # Validaciones
    └── signals.py      # Auditoría automática
```

## Tablas Creadas en PostgreSQL (Neon)

### Total: 10 nuevas tablas

1. **campaigns** - Campañas agrícolas con metas y fechas
2. **campaigns_parcels** - Relación M2M campañas-parcelas
3. **campaigns_partners** - Relación M2M campañas-socios
4. **activity_types** - Tipos de labores (siembra, riego, etc.)
5. **farm_activities** - Registro de labores realizadas
6. **inventory_categories** - Categorías de inventario
7. **inventory_items** - Items de inventario (semillas, pesticidas, fertilizantes)
8. **inventory_movements** - Movimientos de entrada/salida
9. **stock_alerts** - Alertas automáticas de stock bajo
10. **harvested_products** - Productos cosechados

## Funcionalidades Implementadas

### ✅ T036 - Gestión de Campañas
- CRUD completo de campañas
- Código único de campaña
- Fechas de inicio y fin
- Metas de área y producción
- Estados: Planificación, Activa, Completada, Cancelada
- Relación M2M con socios y parcelas
- Acciones: activar, completar, cancelar
- Reporte de campaña

### ✅ T037 - Relación Campaña-Socio
- Tabla intermedia `campaigns_partners`
- Múltiples socios por campaña
- Múltiples campañas por socio
- Filtrado de campañas por socio

### ✅ T038 - Registro de Labores
- 6 tipos de labores predefinidos:
  - Siembra
  - Riego
  - Fertilización
  - Control de Plagas
  - Cosecha
  - Otra
- CRUD completo de labores
- Fecha programada y fecha real
- Cantidad, área cubierta, trabajadores
- Horas trabajadas
- Estados: Pendiente, En Progreso, Completada, Cancelada
- Observaciones y condiciones climáticas

### ✅ T039 - Reporte de Labores por Campaña
- Total de labores
- Labores por tipo
- Labores por estado
- Total de horas trabajadas
- Endpoint: `/api/farm-activities/activities/report_by_campaign/?campaign_id=1`

### ✅ T040 - Catálogo de Inventario de Semillas
- Modelo completo de InventoryItem
- Campos específicos para semillas:
  - Especie
  - Variedad
  - Porcentaje de germinación
  - Fecha de vencimiento
- Categoría "SEED" predefinida

### ✅ T041 - CRUD de Semillas
- Código único
- Especie, variedad, cantidad
- Fecha de vencimiento
- Porcentaje de germinación (PG%)
- Stock actual, mínimo y máximo
- Precio unitario
- Unidad de medida

### ✅ T042 - Gestión de Inventario de Pesticidas
- Categoría "PESTICIDE" predefinida
- Marca, descripción
- Stock y alertas
- Fecha de vencimiento

### ✅ T043 - Tabla de Movimientos de Inventario
- Tipos: Entrada, Salida, Ajuste
- Fecha y referencia
- Motivo del movimiento
- Costo unitario y total
- Actualización automática de stock
- Validación de stock suficiente para salidas

### ✅ T044 & T048 - Alerta de Stock Mínimo (WEB/MÓVIL)
- Creación automática de alertas
- Detección cuando stock <= stock mínimo
- Estado: resuelta/no resuelta
- Endpoint: `/api/inventory/alerts/`
- Endpoint: `/api/inventory/items/low_stock_items/`

### ✅ T045 - Gestión de Inventario de Fertilizantes
- Categoría "FERTILIZER" predefinida
- Mismas funcionalidades que semillas y pesticidas

### ✅ T046 - Reporte de Inventario con Movimientos
- Total de entradas
- Total de salidas
- Total de movimientos
- Filtrado por item
- Endpoint: `/api/inventory/movements/report/`

### ✅ T047 - Consulta de Disponibilidad de Insumos
- Endpoint: `/api/inventory/items/availability/`
- Filtrado por categoría
- Muestra: código, nombre, stock actual, estado
- Estados: OUT_OF_STOCK, LOW_STOCK, NORMAL

### ✅ T049 - Registro de Productos Cosechados
- Por campaña y parcela
- Nombre del producto
- Fecha de cosecha
- Cantidad (kg)
- Grado de calidad
- Porcentaje de humedad
- Temperatura
- Ubicación de almacenamiento
- Cálculo automático de rendimiento por hectárea

### ✅ T050 - Reporte de Producción por Campaña
- Total de cantidad cosechada
- Total de productos
- Producción por parcela
- Producción por socio
- Rendimiento promedio
- Endpoint: `/api/production/harvested-products/report_by_campaign/?campaign_id=1`

### ✅ T052 - Reporte de Producción por Parcela
- Total de cantidad cosechada
- Total de cosechas
- Producción por campaña
- Producción por tipo de producto
- Endpoint: `/api/production/harvested-products/report_by_parcel/?parcel_id=1`

## Endpoints de la API

### Campañas
- `GET /api/campaigns/campaigns/` - Listar
- `POST /api/campaigns/campaigns/` - Crear
- `GET /api/campaigns/campaigns/{id}/` - Detalle
- `PUT/PATCH /api/campaigns/campaigns/{id}/` - Actualizar
- `DELETE /api/campaigns/campaigns/{id}/` - Eliminar
- `POST /api/campaigns/campaigns/{id}/activate/` - Activar
- `POST /api/campaigns/campaigns/{id}/complete/` - Completar
- `POST /api/campaigns/campaigns/{id}/cancel/` - Cancelar
- `GET /api/campaigns/campaigns/{id}/report/` - Reporte

### Labores Agrícolas
- `GET /api/farm-activities/activity-types/` - Tipos de labor
- `GET /api/farm-activities/activities/` - Listar labores
- `POST /api/farm-activities/activities/` - Crear labor
- `GET /api/farm-activities/activities/{id}/` - Detalle
- `PUT/PATCH /api/farm-activities/activities/{id}/` - Actualizar
- `DELETE /api/farm-activities/activities/{id}/` - Eliminar
- `POST /api/farm-activities/activities/{id}/complete/` - Completar
- `GET /api/farm-activities/activities/report_by_campaign/` - Reporte

### Inventario
- `GET /api/inventory/categories/` - Categorías
- `GET /api/inventory/items/` - Listar items
- `POST /api/inventory/items/` - Crear item
- `GET /api/inventory/items/{id}/` - Detalle
- `PUT/PATCH /api/inventory/items/{id}/` - Actualizar
- `DELETE /api/inventory/items/{id}/` - Eliminar
- `GET /api/inventory/items/low_stock_items/` - Items con stock bajo
- `GET /api/inventory/items/availability/` - Disponibilidad
- `GET /api/inventory/movements/` - Listar movimientos
- `POST /api/inventory/movements/` - Crear movimiento
- `GET /api/inventory/movements/report/` - Reporte
- `GET /api/inventory/alerts/` - Listar alertas
- `POST /api/inventory/alerts/{id}/resolve/` - Resolver alerta

### Producción
- `GET /api/production/harvested-products/` - Listar productos
- `POST /api/production/harvested-products/` - Registrar producto
- `GET /api/production/harvested-products/{id}/` - Detalle
- `PUT/PATCH /api/production/harvested-products/{id}/` - Actualizar
- `DELETE /api/production/harvested-products/{id}/` - Eliminar
- `GET /api/production/harvested-products/report_by_campaign/` - Reporte por campaña
- `GET /api/production/harvested-products/report_by_parcel/` - Reporte por parcela

## Filtros Disponibles

### Campañas
- `?search=texto` - Buscar por código, nombre, descripción
- `?status=ACTIVE` - Filtrar por estado
- `?partner=1` - Filtrar por socio
- `?year=2025` - Filtrar por año

### Labores
- `?campaign=1` - Por campaña
- `?parcel=1` - Por parcela
- `?activity_type=1` - Por tipo de labor
- `?status=PENDING` - Por estado
- `?date_from=2025-01-01` - Desde fecha
- `?date_to=2025-12-31` - Hasta fecha

### Inventario
- `?category=1` - Por categoría
- `?search=texto` - Buscar por código, nombre, especie
- `?low_stock=true` - Solo items con stock bajo
- `?is_active=true` - Solo activos

### Movimientos
- `?item=1` - Por item
- `?movement_type=ENTRY` - Por tipo
- `?date_from=2025-01-01` - Desde fecha
- `?date_to=2025-12-31` - Hasta fecha

### Producción
- `?campaign=1` - Por campaña
- `?parcel=1` - Por parcela
- `?partner=1` - Por socio
- `?date_from=2025-01-01` - Desde fecha
- `?date_to=2025-12-31` - Hasta fecha

## Validaciones Implementadas

### Campañas
- Código único
- Fecha de fin posterior a fecha de inicio
- Validación de parcelas y socios existentes

### Labores
- Fecha real no anterior a fecha programada
- Campaña y parcela deben existir

### Inventario
- Código único de item
- Stock suficiente para salidas
- Cantidades positivas
- Alertas automáticas cuando stock <= mínimo

### Producción
- Parcela debe pertenecer a la campaña
- Cantidades positivas
- Fechas válidas

## Características Técnicas

✅ **Clean Code** - Código limpio y organizado
✅ **Arquitectura** - Separación por apps y responsabilidades
✅ **Auditoría** - Registro automático de todas las operaciones
✅ **Validaciones** - En serializers y modelos
✅ **Signals** - Para acciones automáticas
✅ **Permisos** - Control de acceso por rol
✅ **Filtros** - Búsquedas avanzadas
✅ **Reportes** - Estadísticas y agregaciones
✅ **Paginación** - 25 elementos por página
✅ **Documentación** - Endpoints documentados

## Datos Iniciales

Ejecutar: `python manage.py init_sprint2_data`

**Crea:**
- 6 tipos de labores
- 5 categorías de inventario

## Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Inicializar datos Sprint 2
python manage.py init_sprint2_data

# Verificar tablas
python test_sprint2_tables.py

# Ejecutar servidor
python manage.py runserver
```

## Próximos Pasos

### Para Frontend Web:
- Conectar con endpoints de campañas
- Interfaz para registro de labores
- Dashboard de inventario con alertas
- Reportes de producción

### Para App Móvil:
- Registro de labores en campo
- Consulta de disponibilidad de insumos
- Registro de cosecha
- Alertas de stock

### Pendientes (fuera de alcance actual):
- T051/T054 - Gestionar Backup (requiere configuración de servidor)
- CU11 - Monitorear Estado de Cultivos (requiere más especificaciones)
- CU16 - Asistente Inteligente (requiere integración con IA)

## Tecnologías

- Django 4.2
- Django REST Framework 3.16
- PostgreSQL (Neon)
- Signals para automatización
- Aggregations para reportes

## Estado del Proyecto

✅ **Sprint 1** - Completado (Usuarios, Socios, Parcelas, Auditoría)
✅ **Sprint 2** - Completado (Campañas, Labores, Inventario, Producción)

**Total de tablas en BD:** 27
**Total de endpoints:** 80+
**Total de apps:** 8

🎉 **Backend completo y listo para conectar con frontend web y móvil!**
