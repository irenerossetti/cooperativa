# 📋 Sprint 2 - Endpoints Disponibles

## 🎯 Campañas Agrícolas

### Listar Campañas (GET ALL)
```
GET /api/campaigns/campaigns/
GET /api/campaigns/campaigns/?search=2025
GET /api/campaigns/campaigns/?status=ACTIVE
GET /api/campaigns/campaigns/?partner=1
GET /api/campaigns/campaigns/?year=2025
```

### Obtener Campaña por ID (GET BY ID)
```
GET /api/campaigns/campaigns/1/
```

### Crear Campaña (POST)
```
POST /api/campaigns/campaigns/
Body: {
  "code": "CAMP2025-01",
  "name": "Campaña Café 2025",
  "description": "Campaña de café para la temporada 2025",
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "target_area": 100.5,
  "target_production": 5000.0,
  "status": "PLANNING",
  "partners": [1, 2, 3],
  "parcels": [1, 2, 3],
  "notes": "Notas adicionales"
}
```

### Actualizar Campaña (PUT/PATCH)
```
PATCH /api/campaigns/campaigns/1/
Body: {"status": "ACTIVE"}
```

### Eliminar Campaña (DELETE)
```
DELETE /api/campaigns/campaigns/1/
```

### Acciones Especiales
```
POST /api/campaigns/campaigns/1/activate/
POST /api/campaigns/campaigns/1/complete/
Body: {"actual_end_date": "2025-12-31"}

POST /api/campaigns/campaigns/1/cancel/
GET /api/campaigns/campaigns/1/report/
```

---

## 🌾 Labores Agrícolas

### Listar Tipos de Labor (GET ALL)
```
GET /api/farm-activities/activity-types/
```

### Listar Labores (GET ALL)
```
GET /api/farm-activities/activities/
GET /api/farm-activities/activities/?campaign=1
GET /api/farm-activities/activities/?parcel=1
GET /api/farm-activities/activities/?activity_type=1
GET /api/farm-activities/activities/?status=PENDING
GET /api/farm-activities/activities/?date_from=2025-01-01
GET /api/farm-activities/activities/?date_to=2025-12-31
```

### Obtener Labor por ID (GET BY ID)
```
GET /api/farm-activities/activities/1/
```

### Crear Labor (POST)
```
POST /api/farm-activities/activities/
Body: {
  "activity_type": 1,
  "campaign": 1,
  "parcel": 1,
  "scheduled_date": "2025-06-15",
  "description": "Siembra de café variedad Caturra",
  "quantity": 50.0,
  "area_covered": 5.5,
  "workers_count": 3,
  "status": "PENDING",
  "observations": "Condiciones climáticas favorables"
}
```

### Actualizar Labor (PUT/PATCH)
```
PATCH /api/farm-activities/activities/1/
Body: {
  "status": "COMPLETED",
  "actual_date": "2025-06-16",
  "hours_worked": 8.5
}
```

### Completar Labor
```
POST /api/farm-activities/activities/1/complete/
Body: {"actual_date": "2025-06-16"}
```

### Reporte de Labores por Campaña
```
GET /api/farm-activities/activities/report_by_campaign/?campaign_id=1
```

---

## 📦 Inventario

### Categorías de Inventario

#### Listar Categorías (GET ALL)
```
GET /api/inventory/categories/
```

### Items de Inventario

#### Listar Items (GET ALL)
```
GET /api/inventory/items/
GET /api/inventory/items/?category=1
GET /api/inventory/items/?search=cafe
GET /api/inventory/items/?low_stock=true
GET /api/inventory/items/?is_active=true
```

#### Obtener Item por ID (GET BY ID)
```
GET /api/inventory/items/1/
```

#### Crear Item (POST)
```
POST /api/inventory/items/
Body: {
  "code": "SEM-CAFE-001",
  "name": "Semilla de Café Arábica",
  "category": 1,
  "species": "Coffea arabica",
  "variety": "Caturra",
  "brand": "Semillas Premium",
  "germination_percentage": 95.5,
  "unit_of_measure": "kg",
  "minimum_stock": 50.0,
  "maximum_stock": 500.0,
  "unit_price": 25.50,
  "expiration_date": "2026-12-31",
  "is_active": true,
  "description": "Semilla certificada de café"
}
```

#### Actualizar Item (PUT/PATCH)
```
PATCH /api/inventory/items/1/
Body: {"minimum_stock": 100.0}
```

#### Items con Stock Bajo
```
GET /api/inventory/items/low_stock_items/
```

#### Consultar Disponibilidad
```
GET /api/inventory/items/availability/
GET /api/inventory/items/availability/?category=SEED
```

### Movimientos de Inventario

#### Listar Movimientos (GET ALL)
```
GET /api/inventory/movements/
GET /api/inventory/movements/?item=1
GET /api/inventory/movements/?movement_type=ENTRY
GET /api/inventory/movements/?date_from=2025-01-01
GET /api/inventory/movements/?date_to=2025-12-31
```

#### Obtener Movimiento por ID (GET BY ID)
```
GET /api/inventory/movements/1/
```

#### Crear Movimiento - Entrada (POST)
```
POST /api/inventory/movements/
Body: {
  "item": 1,
  "movement_type": "ENTRY",
  "quantity": 100.0,
  "date": "2025-06-01",
  "reference": "Compra #001",
  "reason": "Compra de semillas para campaña 2025",
  "unit_cost": 25.50,
  "total_cost": 2550.00
}
```

#### Crear Movimiento - Salida (POST)
```
POST /api/inventory/movements/
Body: {
  "item": 1,
  "movement_type": "EXIT",
  "quantity": 20.0,
  "date": "2025-06-15",
  "reference": "Siembra Parcela P001",
  "reason": "Uso en siembra de campaña CAMP2025-01"
}
```

#### Reporte de Movimientos
```
GET /api/inventory/movements/report/
GET /api/inventory/movements/report/?item_id=1
```

### Alertas de Stock

#### Listar Alertas (GET ALL)
```
GET /api/inventory/alerts/
GET /api/inventory/alerts/?is_resolved=false
```

#### Obtener Alerta por ID (GET BY ID)
```
GET /api/inventory/alerts/1/
```

#### Resolver Alerta
```
POST /api/inventory/alerts/1/resolve/
```

---

## 🌽 Producción

### Productos Cosechados

#### Listar Productos (GET ALL)
```
GET /api/production/harvested-products/
GET /api/production/harvested-products/?campaign=1
GET /api/production/harvested-products/?parcel=1
GET /api/production/harvested-products/?partner=1
GET /api/production/harvested-products/?date_from=2025-01-01
GET /api/production/harvested-products/?date_to=2025-12-31
```

#### Obtener Producto por ID (GET BY ID)
```
GET /api/production/harvested-products/1/
```

#### Registrar Producto Cosechado (POST)
```
POST /api/production/harvested-products/
Body: {
  "campaign": 1,
  "parcel": 1,
  "partner": 1,
  "product_name": "Café Pergamino",
  "harvest_date": "2025-11-15",
  "quantity": 500.0,
  "quality_grade": "A",
  "moisture_percentage": 12.5,
  "temperature": 22.0,
  "storage_location": "Almacén Central",
  "observations": "Cosecha de excelente calidad"
}
```

#### Actualizar Producto (PUT/PATCH)
```
PATCH /api/production/harvested-products/1/
Body: {"storage_location": "Almacén 2"}
```

#### Eliminar Producto (DELETE)
```
DELETE /api/production/harvested-products/1/
```

#### Reporte de Producción por Campaña
```
GET /api/production/harvested-products/report_by_campaign/?campaign_id=1
```

**Respuesta:**
```json
{
  "total_quantity": 5000.0,
  "total_products": 10,
  "by_parcel": [
    {"parcel__code": "P001", "total": 500.0, "count": 2},
    {"parcel__code": "P002", "total": 800.0, "count": 3}
  ],
  "by_partner": [
    {"partner__first_name": "Juan", "partner__last_name": "Pérez", "total": 1200.0, "count": 4}
  ],
  "average_yield": 500.0
}
```

#### Reporte de Producción por Parcela
```
GET /api/production/harvested-products/report_by_parcel/?parcel_id=1
```

**Respuesta:**
```json
{
  "total_quantity": 500.0,
  "total_harvests": 2,
  "by_campaign": [
    {"campaign__name": "Campaña Café 2025", "total": 500.0, "count": 2}
  ],
  "by_product": [
    {"product_name": "Café Pergamino", "total": 500.0, "count": 2}
  ]
}
```

---

## 📊 Resumen de Endpoints por Módulo

### Campañas
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Filtros: búsqueda, estado, socio, año
- ✅ Acciones: activar, completar, cancelar
- ✅ Reporte de campaña

### Labores Agrícolas
- ✅ CRUD completo
- ✅ Filtros: campaña, parcela, tipo, estado, fechas
- ✅ Acción: completar labor
- ✅ Reporte por campaña

### Inventario
- ✅ CRUD completo de items
- ✅ CRUD completo de movimientos
- ✅ Categorías predefinidas
- ✅ Alertas de stock automáticas
- ✅ Consulta de disponibilidad
- ✅ Items con stock bajo
- ✅ Reporte de movimientos

### Producción
- ✅ CRUD completo de productos cosechados
- ✅ Filtros: campaña, parcela, socio, fechas
- ✅ Reporte por campaña
- ✅ Reporte por parcela
- ✅ Cálculo automático de rendimiento por hectárea

---

## 🔍 Validaciones Implementadas

### Campañas
- Código único
- Fecha de fin posterior a fecha de inicio
- Validación de parcelas y socios

### Labores
- Fecha real no anterior a fecha programada
- Validación de campaña y parcela

### Inventario
- Código único de item
- Stock suficiente para salidas
- Alertas automáticas de stock bajo
- Actualización automática de stock en movimientos

### Producción
- Parcela debe pertenecer a la campaña
- Validación de cantidades positivas
- Cálculo automático de rendimiento

---

## 🎯 Casos de Uso Implementados

✅ **CU7** - Registrar Características de Semillas (catálogo completo)
✅ **CU8** - Registrar Características de Insumos (fertilizantes, pesticidas)
✅ **CU9** - Registrar Campañas Agrícolas (definir metas, fechas y asociar parcelas/socios)
✅ **CU10** - Gestionar Labores Agrícolas (siembra, riego, fertilización, cosecha)
✅ **CU12** - Gestionar Inventario de Insumos (entradas, salidas, ajustes de stock)
✅ **CU13** - Configurar Alertas de Stock Mínimo
✅ **CU14** - Consultar Disponibilidad de Insumos y Productos
✅ **CU15** - Registrar Productos Cosechados

---

## 🚀 Próximos Pasos

Para el frontend/móvil, todos los endpoints están listos para:
- Crear campañas y asignar socios/parcelas
- Registrar labores agrícolas diarias
- Gestionar inventario con alertas automáticas
- Registrar producción y generar reportes
- Consultar disponibilidad de insumos
- Ver reportes de producción por campaña/parcela
