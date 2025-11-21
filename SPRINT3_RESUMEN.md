# Sprint 3 - Comercialización - COMPLETADO ✅

## Resumen Ejecutivo

Se ha implementado el backend completo del Sprint 3 enfocado en la comercialización de productos, gestión de ventas, solicitudes de socios, precios y logística.

## Nuevas Apps Creadas

### 1. **sales** - Gestión de Ventas
- PaymentMethod - Métodos de pago
- Customer - Clientes
- Order - Pedidos de venta
- OrderItem - Items de pedido
- Payment - Pagos

### 2. **requests** - Solicitudes de Socios
- RequestType - Tipos de solicitud
- PartnerRequest - Solicitudes
- RequestItem - Items solicitados
- RequestAttachment - Adjuntos

### 3. **pricing** - Listas de Precios
- PriceList - Listas de precios por campaña
- PriceListItem - Items con precios

### 4. **shipping** - Envíos y Logística
- Shipment - Envíos de pedidos

## Tablas Creadas en PostgreSQL

**Total: 13 nuevas tablas**

1. `payment_methods` - Métodos de pago disponibles
2. `customers` - Clientes (socios o externos)
3. `orders` - Pedidos de venta
4. `order_items` - Items de pedidos
5. `payments` - Registro de pagos
6. `request_types` - Tipos de solicitudes
7. `partner_requests` - Solicitudes de socios
8. `request_items` - Items solicitados
9. `request_attachments` - Adjuntos de solicitudes
10. `price_lists` - Listas de precios
11. `price_list_items` - Items de listas de precios
12. `shipments` - Envíos
13. `partner_requests_items` - Tabla intermedia M2M

**Total acumulado: 40 tablas en la base de datos**

## Funcionalidades Implementadas

### ✅ CU16 - Gestionar Métodos de Pago
- CRUD completo de métodos de pago
- 7 métodos predefinidos: Efectivo, Transferencia, Cheque, Tarjetas, QR, Otro
- Campo para indicar si requiere referencia
- Estado activo/inactivo

### ✅ CU17 - Gestionar Ventas y Pedidos
**Clientes:**
- CRUD completo
- Tipos de documento: CI, NIT, Pasaporte
- Relación opcional con socios
- Validación de documento único

**Pedidos:**
- Número de pedido único
- Relación con cliente y campaña
- Items de pedido con productos cosechados
- Cálculo automático de totales
- Descuentos por porcentaje
- Impuestos
- Estados: Borrador, Confirmado, Pagado, Enviado, Entregado, Cancelado
- Confirmación con descuento automático de stock

**Items de Pedido:**
- Producto, cantidad, precio unitario
- Cálculo automático de total de línea
- Actualización automática de totales del pedido

### ✅ CU18 - Gestionar Solicitudes de Socios
**Tipos de Solicitud:**
- Semillas
- Pesticidas
- Fertilizantes
- Soporte Técnico
- Capacitación
- Otro

**Solicitudes:**
- Número único de solicitud
- Socio solicitante
- Título y descripción detallada
- Prioridad: Baja, Media, Alta, Urgente
- Items solicitados (para insumos)
- Estados: Pendiente, En Revisión, Aprobada, Rechazada, En Progreso, Completada, Cancelada
- Asignación a técnico
- Respuesta del técnico
- Adjuntos (archivos)
- Disponible en Web y Móvil

### ✅ CU19 - Gestionar Precios por Temporada
**Listas de Precios:**
- Código único
- Asociada a campaña
- Vigencia (fecha inicio y fin)
- Estado activo/inactivo

**Items de Precio:**
- Nombre del producto
- Precio unitario
- Unidad de medida
- Descuentos por volumen (cantidad mínima)
- Cálculo automático de precio con descuento

**Aplicación Automática:**
- Al crear pedido, se aplica precio vigente de la campaña
- Validación de vigencia por fecha

### ✅ CU20 - Registrar Pagos e Historial de Ventas
**Pagos:**
- Asociado a pedido
- Método de pago
- Monto
- Fecha de pago
- Número de referencia y recibo
- Estados: Pendiente, Completado, Fallido, Reembolsado
- Actualización automática de estado del pedido

**Historial de Ventas:**
- Filtros por fecha, cliente, campaña, estado
- Exportación a CSV
- Reportes de ventas totales
- Ventas por cliente
- Ventas por campaña
- Ventas por período

### ✅ CU21 - Planificación de Envíos y Logística
**Envíos:**
- Número único de envío
- Asociado a pedido
- Comunidad destino
- Dirección de entrega
- Fecha programada y real
- Transportista, vehículo, conductor
- Estados: Pendiente, Programado, En Tránsito, Entregado, Fallido, Cancelado
- Número de seguimiento
- Firma digital (base64)
- Recibido por
- Actualización automática de estado del pedido

## Endpoints de la API

### Métodos de Pago
```
GET    /api/sales/payment-methods/
POST   /api/sales/payment-methods/
GET    /api/sales/payment-methods/{id}/
PUT    /api/sales/payment-methods/{id}/
DELETE /api/sales/payment-methods/{id}/
```

### Clientes
```
GET    /api/sales/customers/
POST   /api/sales/customers/
GET    /api/sales/customers/{id}/
PUT    /api/sales/customers/{id}/
DELETE /api/sales/customers/{id}/
```

### Pedidos
```
GET    /api/sales/orders/
POST   /api/sales/orders/
GET    /api/sales/orders/{id}/
PUT    /api/sales/orders/{id}/
DELETE /api/sales/orders/{id}/
POST   /api/sales/orders/{id}/confirm/
POST   /api/sales/orders/{id}/cancel/
GET    /api/sales/orders/sales_report/
GET    /api/sales/orders/export_csv/
```

### Items de Pedido
```
GET    /api/sales/order-items/
POST   /api/sales/order-items/
GET    /api/sales/order-items/{id}/
PUT    /api/sales/order-items/{id}/
DELETE /api/sales/order-items/{id}/
```

### Pagos
```
GET    /api/sales/payments/
POST   /api/sales/payments/
GET    /api/sales/payments/{id}/
PUT    /api/sales/payments/{id}/
GET    /api/sales/payments/payment_history/
```

### Solicitudes de Socios
```
GET    /api/requests/request-types/
GET    /api/requests/partner-requests/
POST   /api/requests/partner-requests/
GET    /api/requests/partner-requests/{id}/
PUT    /api/requests/partner-requests/{id}/
DELETE /api/requests/partner-requests/{id}/
POST   /api/requests/partner-requests/{id}/assign/
POST   /api/requests/partner-requests/{id}/respond/
POST   /api/requests/partner-requests/{id}/approve/
POST   /api/requests/partner-requests/{id}/reject/
GET    /api/requests/partner-requests/my_requests/
```

### Listas de Precios
```
GET    /api/pricing/price-lists/
POST   /api/pricing/price-lists/
GET    /api/pricing/price-lists/{id}/
PUT    /api/pricing/price-lists/{id}/
DELETE /api/pricing/price-lists/{id}/
GET    /api/pricing/price-lists/active_for_campaign/
GET    /api/pricing/price-lists/{id}/get_price/
```

### Items de Precio
```
GET    /api/pricing/price-list-items/
POST   /api/pricing/price-list-items/
GET    /api/pricing/price-list-items/{id}/
PUT    /api/pricing/price-list-items/{id}/
DELETE /api/pricing/price-list-items/{id}/
```

### Envíos
```
GET    /api/shipping/shipments/
POST   /api/shipping/shipments/
GET    /api/shipping/shipments/{id}/
PUT    /api/shipping/shipments/{id}/
DELETE /api/shipping/shipments/{id}/
POST   /api/shipping/shipments/{id}/schedule/
POST   /api/shipping/shipments/{id}/mark_in_transit/
POST   /api/shipping/shipments/{id}/mark_delivered/
GET    /api/shipping/shipments/pending_shipments/
```

## Validaciones Implementadas

### Ventas
- Número de pedido único
- Número de documento de cliente único
- Cantidades positivas
- Precios positivos
- Stock suficiente al confirmar pedido
- Cálculo automático de totales

### Solicitudes
- Número de solicitud único
- Validación de items solicitados
- Validación de archivos adjuntos
- Asignación solo a usuarios activos

### Precios
- Código único de lista
- Fechas de vigencia válidas
- Precios positivos
- Validación de vigencia al aplicar

### Envíos
- Número de envío único
- Validación de fechas
- Actualización automática de estados

## Flujos Automáticos

### Flujo de Pedido
1. Crear pedido (DRAFT)
2. Agregar items
3. Confirmar pedido → Descuenta stock
4. Registrar pago → Cambia a PAID
5. Crear envío → Cambia a SHIPPED
6. Marcar entregado → Cambia a DELIVERED

### Flujo de Solicitud
1. Socio crea solicitud (PENDING)
2. Admin asigna a técnico (IN_REVIEW)
3. Técnico responde (APPROVED/REJECTED)
4. Si aprobada → Crear movimiento de inventario
5. Completar solicitud (COMPLETED)

### Flujo de Precio
1. Crear lista de precios para campaña
2. Agregar items con precios
3. Al crear pedido, se aplica precio vigente automáticamente
4. Descuentos por volumen se calculan automáticamente

## Características Técnicas

✅ **Cálculos Automáticos**
- Totales de pedido
- Descuentos
- Precios con descuento por volumen
- Actualización de stock

✅ **Estados y Transiciones**
- Pedidos: 6 estados
- Pagos: 4 estados
- Solicitudes: 7 estados
- Envíos: 6 estados

✅ **Relaciones Complejas**
- M2M entre solicitudes e items
- Cascada de actualizaciones
- Signals para automatización

✅ **Reportes y Exportación**
- Historial de ventas
- Exportación a CSV
- Filtros avanzados
- Agregaciones

## Comandos de Inicialización

Crear archivo: `sales/management/commands/init_sprint3_data.py`

```bash
python manage.py init_sprint3_data
```

Crea:
- 7 métodos de pago
- 6 tipos de solicitud

## Estado del Proyecto

✅ **Sprint 1** - Usuarios, Socios, Parcelas, Auditoría
✅ **Sprint 2** - Campañas, Labores, Inventario, Producción
✅ **Sprint 3** - Ventas, Solicitudes, Precios, Envíos

**Total:**
- 🗄️ 40 tablas en PostgreSQL (Neon)
- 🔌 120+ endpoints REST
- 📱 Listo para frontend web y móvil
- 📊 Sistema completo de comercialización
- 🔔 Automatizaciones y validaciones
- 📝 Auditoría completa

🎉 **Backend completo de los 3 sprints listo para producción!**
