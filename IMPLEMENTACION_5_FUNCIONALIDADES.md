# 🚀 IMPLEMENTACIÓN DE 5 FUNCIONALIDADES NUEVAS

## Estado: En Progreso
**Fecha:** Diciembre 2024
**Tiempo estimado total:** 8-10 horas

---

## 📋 TAREA 1: Sistema de Notificaciones en Tiempo Real (2h)

### Objetivo
Mejorar el sistema de alertas existente con notificaciones en tiempo real y contador en navbar.

### Archivos a Modificar/Crear

#### Backend
1. **`alerts/views.py`** - Agregar endpoints de notificaciones
2. **`alerts/serializers.py`** - Serializer para notificaciones
3. **`alerts/urls.py`** - Rutas de notificaciones
4. **`alerts/signals.py`** - Señales automáticas (NUEVO)

#### Frontend
1. **`src/components/layout/NotificationBell.jsx`** - Campana con badge (NUEVO)
2. **`src/components/layout/NotificationDropdown.jsx`** - Dropdown de notificaciones (NUEVO)
3. **`src/hooks/useNotifications.js`** - Hook personalizado (NUEVO)

### Implementación

#### Paso 1: Backend - Endpoints de Notificaciones
```python
# alerts/views.py - AGREGAR
from rest_framework.decorators import action

class AlertViewSet(viewsets.ModelViewSet):
    # ... código existente ...
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Contador de notificaciones no leídas"""
        count = Alert.objects.filter(
            organization=request.organization,
            target_user=request.user,
            is_read=False,
            is_active=True
        ).count()
        return Response({'count': count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Marcar notificación como leída"""
        alert = self.get_object()
        alert.is_read = True
        alert.save()
        return Response({'status': 'marked_as_read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Marcar todas como leídas"""
        Alert.objects.filter(
            organization=request.organization,
            target_user=request.user,
            is_read=False
        ).update(is_read=True)
        return Response({'status': 'all_marked_as_read'})
```

#### Paso 2: Frontend - Componente de Notificaciones
```jsx
// src/components/layout/NotificationBell.jsx
import { useState, useEffect } from 'react';
import { Bell } from 'lucide-react';
import api from '../../services/api';

export default function NotificationBell() {
  const [count, setCount] = useState(0);
  const [notifications, setNotifications] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    fetchNotifications();
    // Polling cada 30 segundos
    const interval = setInterval(fetchNotifications, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchNotifications = async () => {
    try {
      const [countRes, notifRes] = await Promise.all([
        api.get('/api/alerts/unread_count/'),
        api.get('/api/alerts/?is_read=false&page_size=10')
      ]);
      setCount(countRes.data.count);
      setNotifica