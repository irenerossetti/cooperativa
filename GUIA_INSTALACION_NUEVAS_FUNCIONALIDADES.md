# 🚀 GUÍA DE INSTALACIÓN - NUEVAS FUNCIONALIDADES

## 📋 Resumen

Se han implementado **7 nuevas funcionalidades** para el sistema:

1. ✅ Sistema de Notificaciones Push Multi-Canal
2. ✅ Generador de Códigos QR para Trazabilidad
3. ⏳ Dashboard de Métricas en Tiempo Real
4. ⏳ Asistente de IA con Chat Conversacional
5. ⏳ Reportes Dinámicos Mejorados
6. ⏳ CRUD: Eventos y Calendario Agrícola
7. ⏳ CRUD: Metas y Objetivos

## 🔧 INSTALACIÓN PASO A PASO

### 1. Instalar Dependencias de Python

```bash
cd cooperativa
pip install qrcode[pil] pillow
```

### 2. Actualizar `requirements.txt`

Agregar al final del archivo:

```txt
# Nuevas funcionalidades
qrcode==7.4.2
Pillow==10.1.0
```

### 3. Actualizar `config/settings.py`

Agregar las nuevas apps a `TENANT_APPS`:

```python
TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    
    # Apps existentes
    'users',
    'partners',
    'parcels',
    'campaigns',
    'farm_activities',
    'inventory',
    'production',
    'sales',
    'requests',
    'pricing',
    'shipping',
    'financial',
    'reports',
    'traceability',
    'analytics',
    'ai_recommendations',
    'monitoring',
    'weather',
    'audit',
    'alerts',
    'market_analysis',
    'chatbot',
    
    # NUEVAS APPS ⭐
    'notifications',
    'qr_codes',
    
    'rest_framework',
]
```

### 4. Actualizar `config/urls.py`

Agregar las nuevas URLs:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs existentes
    path('api/auth/', include('users.urls')),
    path('api/partners/', include('partners.urls')),
    path('api/parcels/', include('parcels.urls')),
    path('api/campaigns/', include('campaigns.urls')),
    path('api/farm-activities/', include('farm_activities.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/production/', include('production.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/requests/', include('requests.urls')),
    path('api/pricing/', include('pricing.urls')),
    path('api/shipping/', include('shipping.urls')),
    path('api/financial/', include('financial.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/traceability/', include('traceability.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/ai/', include('ai_recommendations.urls')),
    path('api/monitoring/', include('monitoring.urls')),
    path('api/weather/', include('weather.urls')),
    path('api/audit/', include('audit.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/market/', include('market_analysis.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/tenants/', include('tenants.urls')),
    
    # NUEVAS URLs ⭐
    path('api/', include('notifications.urls')),
    path('api/', include('qr_codes.urls')),
]
```

### 5. Crear Migraciones

```bash
# Crear migraciones para las nuevas apps
python manage.py makemigrations notifications qr_codes

# Aplicar migraciones
python manage.py migrate
```

### 6. Crear Datos de Prueba (Opcional)

Crear archivo `create_test_notifications.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from notifications.utils import create_notification, notify_admins
from users.models import User

# Crear notificaciones de prueba
users = User.objects.filter(is_active=True)[:3]

for user in users:
    # Notificación de información
    create_notification(
        user=user,
        title='Bienvenido al sistema de notificaciones',
        message='Ahora recibirás notificaciones en tiempo real sobre eventos importantes',
        notification_type='INFO'
    )
    
    # Notificación de éxito
    create_notification(
        user=user,
        title='Sistema actualizado',
        message='El sistema ha sido actualizado con nuevas funcionalidades',
        notification_type='SUCCESS'
    )

# Notificar a todos los admins
notify_admins(
    title='Nuevas funcionalidades disponibles',
    message='Se han agregado notificaciones y códigos QR al sistema',
    notification_type='INFO'
)

print("✅ Notificaciones de prueba creadas")
```

Ejecutar:
```bash
python create_test_notifications.py
```

## 🎨 INTEGRACIÓN EN FRONTEND

### 1. Agregar NotificationBell al Navbar

Editar `cooperativa_frontend/src/components/layout/Navbar.jsx`:

```jsx
import NotificationBell from '../notifications/NotificationBell';

// Dentro del componente, agregar antes del menú de usuario:
<div className="flex items-center gap-4">
  {/* Notificaciones */}
  <NotificationBell />
  
  {/* Usuario (existente) */}
  <div className="relative">
    {/* ... código existente del menú de usuario */}
  </div>
</div>
```

### 2. Agregar Ruta de Notificaciones

Editar `cooperativa_frontend/src/App.jsx`:

```jsx
import NotificationsPage from './pages/NotificationsPage';

// Agregar en las rutas protegidas:
<Route path="/notifications" element={<NotificationsPage />} />
```

### 3. Agregar Botones QR en Listas

Ejemplo en `cooperativa_frontend/src/pages/Socios.jsx`:

```jsx
import { QrCode } from 'lucide-react';
import { useState } from 'react';
import QRCodeModal from '../components/qr/QRCodeModal';

const Socios = () => {
  const [qrModal, setQrModal] = useState({ show: false, partner: null });
  
  // ... código existente
  
  return (
    <div>
      {/* ... código existente */}
      
      {/* En la tabla, agregar columna de acciones: */}
      <td className="px-6 py-4">
        <div className="flex gap-2">
          {/* Botones existentes */}
          
          {/* NUEVO: Botón QR */}
          <button
            onClick={() => setQrModal({ show: true, partner: socio })}
            className="p-2 text-blue-400 hover:bg-gray-700 rounded-lg transition"
            title="Ver código QR"
          >
            <QrCode className="w-4 h-4" />
          </button>
        </div>
      </td>
      
      {/* Modal QR */}
      {qrModal.show && (
        <QRCodeModal
          isOpen={qrModal.show}
          onClose={() => setQrModal({ show: false, partner: null })}
          modelType="partner"
          objectId={qrModal.partner?.id}
          objectName={qrModal.partner?.full_name}
        />
      )}
    </div>
  );
};
```

## 🧪 PRUEBAS

### 1. Probar Notificaciones

#### Desde Python Shell:
```bash
python manage.py shell
```

```python
from notifications.utils import create_notification
from users.models import User

user = User.objects.first()
create_notification(
    user=user,
    title='Prueba de notificación',
    message='Esta es una notificación de prueba',
    notification_type='SUCCESS'
)
```

#### Desde API (Postman/cURL):
```bash
curl -X POST http://localhost:8000/api/notifications/notifications/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "title": "Prueba desde API",
    "message": "Notificación creada desde la API",
    "type": "INFO"
  }'
```

#### Verificar en Frontend:
1. Abre http://localhost:5173
2. Verás el badge con el número de notificaciones
3. Click en la campana
4. Deberías ver las notificaciones

### 2. Probar Códigos QR

#### Generar QR desde API:
```bash
curl -X POST http://localhost:8000/api/qr-codes/qr-codes/generate/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_type": "partner",
    "object_id": 1,
    "include_data": true
  }'
```

#### Verificar en Frontend:
1. Ve a la lista de socios
2. Click en el botón QR de cualquier socio
3. Deberías ver el modal con el código QR
4. Prueba descargar, compartir e imprimir

### 3. Escanear QR con Celular

1. Genera un QR desde la UI
2. Descarga la imagen
3. Escanea con la cámara de tu celular
4. Te llevará a la URL de escaneo
5. Verás los datos del socio/parcela/producto

## 🔗 INTEGRAR NOTIFICACIONES EN EVENTOS

### Ejemplo: Notificar al crear una venta

Editar `cooperativa/sales/views.py`:

```python
from notifications.utils import notify_admins, create_notification

class OrderViewSet(viewsets.ModelViewSet):
    # ... código existente
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        order = self.get_object()
        
        # Notificar a administradores
        notify_admins(
            title='Nueva venta registrada',
            message=f'Se ha registrado una venta por Bs. {order.total_amount}',
            notification_type='SALE',
            extra_data={
                'order_id': order.id,
                'amount': float(order.total_amount)
            }
        )
        
        # Notificar al cliente (si tiene usuario)
        if order.customer and hasattr(order.customer, 'user'):
            create_notification(
                user=order.customer.user,
                title='Pedido confirmado',
                message=f'Tu pedido #{order.order_number} ha sido confirmado',
                notification_type='SUCCESS',
                action_url=f'/orders/{order.id}'
            )
        
        return response
```

### Ejemplo: Notificar stock bajo

Editar `cooperativa/inventory/views.py`:

```python
from notifications.utils import notify_admins
from django.db.models import F

class InventoryItemViewSet(viewsets.ModelViewSet):
    # ... código existente
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        item = self.get_object()
        
        # Verificar si el stock está bajo
        if item.current_stock <= item.min_stock:
            notify_admins(
                title='Alerta de stock bajo',
                message=f'El item "{item.name}" tiene stock bajo ({item.current_stock} unidades)',
                notification_type='STOCK',
                extra_data={
                    'item_id': item.id,
                    'current_stock': item.current_stock,
                    'min_stock': item.min_stock
                }
            )
        
        return response
```

## 📱 INTEGRACIÓN EN APP MÓVIL (Flutter)

### 1. Agregar Notificaciones

Crear `lib/features/notifications/data/models/notification_model.dart`:

```dart
class NotificationModel {
  final int id;
  final String title;
  final String message;
  final String type;
  final bool read;
  final DateTime createdAt;
  final String? actionUrl;
  
  NotificationModel({
    required this.id,
    required this.title,
    required this.message,
    required this.type,
    required this.read,
    required this.createdAt,
    this.actionUrl,
  });
  
  factory NotificationModel.fromJson(Map<String, dynamic> json) {
    return NotificationModel(
      id: json['id'],
      title: json['title'],
      message: json['message'],
      type: json['type'],
      read: json['read'],
      createdAt: DateTime.parse(json['created_at']),
      actionUrl: json['action_url'],
    );
  }
}
```

### 2. Agregar Escaneo de QR

Agregar dependencia en `pubspec.yaml`:

```yaml
dependencies:
  qr_code_scanner: ^1.0.1
```

Crear pantalla de escaneo:

```dart
import 'package:qr_code_scanner/qr_code_scanner.dart';

class QRScannerScreen extends StatefulWidget {
  @override
  _QRScannerScreenState createState() => _QRScannerScreenState();
}

class _QRScannerScreenState extends State<QRScannerScreen> {
  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');
  QRViewController? controller;
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Escanear QR')),
      body: QRView(
        key: qrKey,
        onQRViewCreated: _onQRViewCreated,
      ),
    );
  }
  
  void _onQRViewCreated(QRViewController controller) {
    this.controller = controller;
    controller.scannedDataStream.listen((scanData) {
      // Procesar datos escaneados
      _handleScannedData(scanData.code);
    });
  }
  
  void _handleScannedData(String? data) {
    if (data != null) {
      // Navegar a la pantalla de detalles
      Navigator.pop(context, data);
    }
  }
}
```

## ✅ CHECKLIST DE INSTALACIÓN

- [ ] Instalar dependencias Python (`qrcode`, `pillow`)
- [ ] Actualizar `requirements.txt`
- [ ] Agregar apps a `TENANT_APPS` en settings
- [ ] Agregar URLs en `config/urls.py`
- [ ] Crear migraciones (`makemigrations`)
- [ ] Aplicar migraciones (`migrate`)
- [ ] Crear datos de prueba (opcional)
- [ ] Integrar `NotificationBell` en Navbar
- [ ] Agregar ruta `/notifications`
- [ ] Agregar botones QR en listas
- [ ] Probar notificaciones desde API
- [ ] Probar generación de QR
- [ ] Escanear QR con celular
- [ ] Integrar notificaciones en eventos del sistema
- [ ] Documentar para el equipo

## 🎓 PARA LA DEFENSA

### Demo Sugerida:

1. **Notificaciones:**
   - Mostrar campana con badge
   - Abrir dropdown
   - Marcar como leída
   - Ir a página completa
   - Filtrar por tipo
   - Marcar todas como leídas

2. **Códigos QR:**
   - Ir a lista de socios
   - Click en botón QR
   - Mostrar modal con QR
   - Descargar QR
   - Compartir URL
   - Imprimir (preview)
   - Escanear con celular (si es posible)

### Puntos a Destacar:

- ✅ **Sistema completo de notificaciones** con 10 tipos diferentes
- ✅ **Actualización automática** cada 30 segundos
- ✅ **Preferencias personalizables** por usuario
- ✅ **Códigos QR para trazabilidad** - cumple estándares internacionales
- ✅ **Contador de escaneos** - métricas de uso
- ✅ **Múltiples formatos** - descargar, compartir, imprimir
- ✅ **Diseño profesional** con animaciones suaves
- ✅ **Integración completa** - backend, frontend y móvil

## 🚀 PRÓXIMOS PASOS

Después de instalar estas funcionalidades, continuar con:

3. Dashboard de Métricas en Tiempo Real
4. Asistente de IA con Chat Conversacional
5. Reportes Dinámicos Mejorados
6. CRUD: Eventos y Calendario Agrícola
7. CRUD: Metas y Objetivos

---

**Tiempo estimado de instalación:** 30-45 minutos  
**Dificultad:** Media  
**Estado:** ✅ Listo para instalar
