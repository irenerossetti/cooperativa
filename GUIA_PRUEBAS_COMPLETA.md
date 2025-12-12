# 🧪 GUÍA COMPLETA DE PRUEBAS

## 📋 Índice
1. [Instalación y Configuración](#instalación-y-configuración)
2. [Pruebas de Backend](#pruebas-de-backend)
3. [Pruebas de Frontend](#pruebas-de-frontend)
4. [Pruebas de Integración](#pruebas-de-integración)
5. [Checklist de Defensa](#checklist-de-defensa)

---

## 🚀 INSTALACIÓN Y CONFIGURACIÓN

### Opción A: Script Automático (Recomendado)

```bash
cd cooperativa
python setup_complete.py
```

Este script:
- ✅ Verifica apps creadas
- ✅ Actualiza settings.py automáticamente
- ✅ Actualiza urls.py automáticamente
- ✅ Instala dependencias
- ✅ Crea y aplica migraciones
- ✅ Crea datos de prueba

### Opción B: Manual

#### 1. Actualizar settings.py

Agregar a `TENANT_APPS`:
```python
TENANT_APPS = [
    # ... apps existentes
    'notifications',
    'qr_codes',
    'dashboard',
    'ai_chat',
    'events',
    'goals',
    'rest_framework',
]
```

#### 2. Actualizar urls.py

Agregar en `config/urls.py`:
```python
urlpatterns = [
    # ... urls existentes
    path('api/', include('notifications.urls')),
    path('api/', include('qr_codes.urls')),
    path('api/', include('dashboard.urls')),
    path('api/ai-chat/', include('ai_chat.urls')),
    path('api/', include('events.urls')),
    path('api/', include('goals.urls')),
]
```

#### 3. Instalar dependencias

```bash
pip install qrcode[pil] pillow requests
```

#### 4. Crear y aplicar migraciones

```bash
python manage.py makemigrations notifications qr_codes ai_chat events goals
python manage.py migrate
```

#### 5. Crear datos de prueba

```bash
python create_test_data_complete.py
```

---

## 🧪 PRUEBAS DE BACKEND

### Prueba Automática

```bash
python test_all_features.py
```

Este script prueba:
- ✅ Notificaciones
- ✅ Códigos QR
- ✅ Dashboard
- ✅ Chat IA
- ✅ Eventos
- ✅ Metas
- ✅ Endpoints

### Pruebas Manuales por Funcionalidad

#### 1. Notificaciones 🔔

**Crear notificación:**
```bash
python manage.py shell
```

```python
from notifications.utils import create_notification
from users.models import User

user = User.objects.first()
notif = create_notification(
    user=user,
    title='Prueba manual',
    message='Esta es una notificación de prueba',
    notification_type='SUCCESS'
)
print(f"Notificación creada: #{notif.id}")
```

**Probar API:**
```bash
# Listar notificaciones
curl http://localhost:8000/api/notifications/notifications/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Contador de no leídas
curl http://localhost:8000/api/notifications/notifications/unread_count/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Marcar como leída
curl -X POST http://localhost:8000/api/notifications/notifications/1/mark_read/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Verificar:**
- [ ] Notificaciones se crean correctamente
- [ ] Contador funciona
- [ ] Marcar como leída funciona
- [ ] Filtros funcionan

---

#### 2. Códigos QR 📱

**Generar QR:**
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

**Obtener imagen:**
```bash
# Abrir en navegador
http://localhost:8000/api/qr-codes/qr-codes/1/image/
```

**Escanear QR:**
```bash
curl http://localhost:8000/api/qr-codes/qr-codes/1/scan/
```

**Verificar:**
- [ ] QR se genera correctamente
- [ ] Imagen PNG se descarga
- [ ] Escaneo incrementa contador
- [ ] Datos se devuelven correctamente

---

#### 3. Dashboard 📊

**Obtener métricas:**
```bash
curl http://localhost:8000/api/dashboard/metrics/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Obtener gráficos:**
```bash
curl http://localhost:8000/api/dashboard/charts/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Verificar:**
- [ ] Métricas se calculan correctamente
- [ ] Gráficos tienen datos
- [ ] Tendencias son correctas
- [ ] Top productos funciona

---

#### 4. Chat IA 💬

**Enviar mensaje:**
```bash
curl -X POST http://localhost:8000/api/ai-chat/conversations/chat/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuántos socios tengo?",
    "include_context": true
  }'
```

**Pregunta rápida:**
```bash
curl -X POST http://localhost:8000/api/ai-chat/quick/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuánto vendí hoy?"
  }'
```

**Verificar:**
- [ ] Respuestas tienen sentido
- [ ] Contexto se incluye
- [ ] Historial se guarda
- [ ] Fallback funciona sin API

---

#### 5. Eventos 📅

**Crear evento:**
```bash
curl -X POST http://localhost:8000/api/events/events/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Siembra de Café",
    "type": "SIEMBRA",
    "start_datetime": "2024-12-15T08:00:00Z",
    "end_datetime": "2024-12-15T12:00:00Z",
    "location": "Parcela Norte",
    "priority": "HIGH"
  }'
```

**Listar próximos:**
```bash
curl http://localhost:8000/api/events/events/upcoming/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Enviar recordatorios:**
```bash
curl -X POST http://localhost:8000/api/events/events/1/send_reminder/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Verificar:**
- [ ] Eventos se crean correctamente
- [ ] Filtros funcionan
- [ ] Recordatorios se envían
- [ ] Calendario funciona

---

#### 6. Metas 🎯

**Crear meta:**
```bash
curl -X POST http://localhost:8000/api/goals/goals/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aumentar Producción",
    "type": "PRODUCTION",
    "target_value": 10000,
    "current_value": 0,
    "unit": "kg",
    "start_date": "2024-12-01",
    "end_date": "2025-03-01",
    "priority": "HIGH"
  }'
```

**Actualizar progreso:**
```bash
curl -X POST http://localhost:8000/api/goals/goals/1/update_progress/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_value": 6500
  }'
```

**Metas en riesgo:**
```bash
curl http://localhost:8000/api/goals/goals/at_risk/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Verificar:**
- [ ] Metas se crean correctamente
- [ ] Progreso se calcula bien
- [ ] Detección de riesgo funciona
- [ ] Estadísticas son correctas

---

## 🎨 PRUEBAS DE FRONTEND

### Instalación Frontend

```bash
cd cooperativa_frontend
npm install recharts
npm run dev
```

### Pruebas por Componente

#### 1. NotificationBell

**Ubicación:** Navbar

**Probar:**
1. [ ] Badge muestra número correcto
2. [ ] Click abre dropdown
3. [ ] Notificaciones se muestran
4. [ ] Marcar como leída funciona
5. [ ] Link a página completa funciona

**Cómo probar:**
1. Crear notificaciones en backend
2. Refrescar página
3. Verificar badge
4. Click en campana
5. Verificar dropdown

---

#### 2. NotificationsPage

**URL:** `/notifications`

**Probar:**
1. [ ] Lista se carga correctamente
2. [ ] Filtros funcionan (all, unread, read)
3. [ ] Filtro por tipo funciona
4. [ ] Marcar como leída funciona
5. [ ] Marcar todas funciona
6. [ ] Eliminar funciona

**Cómo probar:**
1. Ir a `/notifications`
2. Verificar lista
3. Probar cada filtro
4. Marcar notificaciones
5. Eliminar notificaciones

---

#### 3. QRCodeModal

**Ubicación:** Lista de socios (agregar botón)

**Probar:**
1. [ ] Modal se abre correctamente
2. [ ] QR se genera y muestra
3. [ ] Descargar funciona
4. [ ] Compartir funciona
5. [ ] Imprimir funciona

**Cómo probar:**
1. Ir a lista de socios
2. Agregar botón QR (ver código abajo)
3. Click en botón
4. Verificar modal
5. Probar acciones

**Código para agregar botón:**
```jsx
// En src/pages/Socios.jsx
import { QrCode } from 'lucide-react';
import QRCodeModal from '../components/qr/QRCodeModal';

const [qrModal, setQrModal] = useState({ show: false, partner: null });

// En la tabla:
<button
  onClick={() => setQrModal({ show: true, partner: socio })}
  className="p-2 text-blue-400 hover:bg-gray-700 rounded-lg"
>
  <QrCode className="w-4 h-4" />
</button>

// Después de la tabla:
{qrModal.show && (
  <QRCodeModal
    isOpen={qrModal.show}
    onClose={() => setQrModal({ show: false, partner: null })}
    modelType="partner"
    objectId={qrModal.partner?.id}
    objectName={qrModal.partner?.full_name}
  />
)}
```

---

#### 4. DashboardRealTime

**URL:** `/dashboard-realtime`

**Probar:**
1. [ ] Métricas se cargan
2. [ ] Actualización automática funciona (5s)
3. [ ] Gráficos se muestran correctamente
4. [ ] Top productos funciona
5. [ ] Actividad reciente funciona

**Cómo probar:**
1. Ir a `/dashboard-realtime`
2. Verificar métricas
3. Esperar 5 segundos
4. Verificar actualización
5. Crear una venta en otra pestaña
6. Verificar que se actualiza

---

#### 5. AIChat

**URL:** `/ai-chat`

**Probar:**
1. [ ] Chat se carga correctamente
2. [ ] Preguntas sugeridas funcionan
3. [ ] Enviar mensaje funciona
4. [ ] Respuestas se muestran
5. [ ] Historial se guarda
6. [ ] Nueva conversación funciona

**Cómo probar:**
1. Ir a `/ai-chat`
2. Click en pregunta sugerida
3. Enviar mensaje
4. Verificar respuesta
5. Crear nueva conversación
6. Verificar historial

**Preguntas de prueba:**
- "¿Cuántos socios tengo?"
- "¿Cuánto vendí hoy?"
- "¿Qué insumos necesito comprar?"
- "¿Cuántas campañas activas tengo?"

---

## 🔗 PRUEBAS DE INTEGRACIÓN

### Flujo Completo 1: Notificación de Venta

1. **Crear venta en el sistema**
2. **Verificar que se crea notificación**
3. **Ver notificación en navbar**
4. **Marcar como leída**
5. **Verificar en página de notificaciones**

### Flujo Completo 2: QR de Socio

1. **Ir a lista de socios**
2. **Generar QR de un socio**
3. **Descargar QR**
4. **Escanear con celular**
5. **Verificar datos del socio**

### Flujo Completo 3: Dashboard en Tiempo Real

1. **Abrir dashboard**
2. **Anotar métricas actuales**
3. **Crear una venta**
4. **Esperar 5 segundos**
5. **Verificar actualización automática**

### Flujo Completo 4: Chat IA

1. **Abrir chat**
2. **Hacer pregunta sobre socios**
3. **Verificar respuesta con datos reales**
4. **Hacer pregunta sobre ventas**
5. **Verificar respuesta**

### Flujo Completo 5: Evento con Recordatorio

1. **Crear evento futuro**
2. **Agregar participantes**
3. **Enviar recordatorios**
4. **Verificar notificaciones creadas**
5. **Verificar en página de notificaciones**

### Flujo Completo 6: Meta con Progreso

1. **Crear meta**
2. **Verificar progreso inicial (0%)**
3. **Actualizar progreso**
4. **Verificar cálculo de porcentaje**
5. **Verificar detección de riesgo**

---

## ✅ CHECKLIST DE DEFENSA

### Antes de la Defensa

#### Backend:
- [ ] Servidor corriendo sin errores
- [ ] Todas las migraciones aplicadas
- [ ] Datos de prueba creados
- [ ] Endpoints respondiendo correctamente
- [ ] Logs sin errores críticos

#### Frontend:
- [ ] Servidor corriendo sin errores
- [ ] Todas las rutas configuradas
- [ ] Componentes renderizando correctamente
- [ ] No hay errores en consola
- [ ] Estilos aplicados correctamente

#### Datos:
- [ ] Al menos 5 notificaciones de prueba
- [ ] Al menos 3 QR codes generados
- [ ] Dashboard con datos reales
- [ ] Al menos 2 conversaciones de IA
- [ ] Al menos 3 eventos creados
- [ ] Al menos 3 metas creadas

#### Documentación:
- [ ] RESUMEN_FINAL_DEFENSA.md leído
- [ ] Guión de presentación preparado
- [ ] Respuestas a preguntas frecuentes revisadas
- [ ] Código comentado y limpio

---

### Durante la Defensa

#### Preparación Técnica:
- [ ] Laptop cargada
- [ ] Internet funcionando
- [ ] Backend corriendo
- [ ] Frontend corriendo
- [ ] Pestañas necesarias abiertas
- [ ] Login realizado
- [ ] Celular listo para escanear QR

#### Demo:
- [ ] Mostrar notificaciones
- [ ] Generar y escanear QR
- [ ] Mostrar dashboard actualizándose
- [ ] Hacer preguntas al chat IA
- [ ] Mostrar calendario de eventos
- [ ] Mostrar metas con progreso

#### Plan B:
- [ ] Screenshots de funcionalidades
- [ ] Video de demo grabado
- [ ] Código fuente disponible
- [ ] Documentación impresa

---

## 🎯 CRITERIOS DE ÉXITO

### Funcionalidad (40%)
- [ ] Todas las funcionalidades funcionan
- [ ] No hay errores críticos
- [ ] Datos se muestran correctamente
- [ ] Integración backend-frontend funciona

### Código (30%)
- [ ] Código bien estructurado
- [ ] Buenas prácticas aplicadas
- [ ] Comentarios donde necesario
- [ ] Sin código duplicado

### Presentación (20%)
- [ ] Explicación clara
- [ ] Demo fluida
- [ ] Respuestas seguras
- [ ] Tiempo adecuado

### Documentación (10%)
- [ ] Documentación completa
- [ ] Casos de uso claros
- [ ] Guías de instalación
- [ ] Comentarios en código

---

## 🚀 COMANDOS RÁPIDOS

### Iniciar Todo

```bash
# Terminal 1: Backend
cd cooperativa
python manage.py runserver

# Terminal 2: Frontend
cd cooperativa_frontend
npm run dev

# Terminal 3: Pruebas
cd cooperativa
python test_all_features.py
```

### Crear Datos de Prueba

```bash
cd cooperativa
python create_test_data_complete.py
```

### Verificar Estado

```bash
cd cooperativa
python test_all_features.py
```

---

## 📚 RECURSOS ADICIONALES

- **Documentación Completa:** `IMPLEMENTACION_FINAL_7_FUNCIONALIDADES.md`
- **Guión de Defensa:** `RESUMEN_FINAL_DEFENSA.md`
- **Instalación:** `GUIA_INSTALACION_NUEVAS_FUNCIONALIDADES.md`

---

**¡Buena suerte en tu defensa!** 🎓🚀
