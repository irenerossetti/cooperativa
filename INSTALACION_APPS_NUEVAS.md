# ✅ Instalación de Nuevas Apps

## 🐛 Error
```
RuntimeError: Model class notifications.models.Notification doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
```

## 🔍 Causa
Las 6 nuevas apps no estaban registradas en `INSTALLED_APPS` del archivo `settings.py`.

## ✅ Solución Aplicada

### Archivo: `config/settings.py`

```python
INSTALLED_APPS = [
    # ... apps existentes ...
    'alerts',
    # Nuevas funcionalidades
    'notifications',
    'qr_codes',
    'dashboard',
    'ai_chat',
    'events',
    'goals',
]
```

## 📋 Apps Agregadas

1. **notifications** - Sistema de notificaciones
2. **qr_codes** - Generación y gestión de códigos QR
3. **dashboard** - Dashboard en tiempo real
4. **ai_chat** - Asistente de IA conversacional
5. **events** - Calendario de eventos
6. **goals** - Metas y objetivos

## 🚀 Próximos Pasos

### 1. Crear Migraciones
```bash
python manage.py makemigrations notifications
python manage.py makemigrations qr_codes
python manage.py makemigrations ai_chat
python manage.py makemigrations events
python manage.py makemigrations goals
```

### 2. Aplicar Migraciones
```bash
python manage.py migrate
```

### 3. Iniciar Servidor
```bash
python manage.py runserver
```

## ✅ Verificación

El servidor debería iniciar sin errores:
```
System check identified no issues (0 silenced).
Django version 4.2.26, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
```

## 📝 Checklist Completo

- [x] Apps agregadas a INSTALLED_APPS
- [x] Imports corregidos (tenants.managers)
- [x] URLs registradas en config/urls.py
- [x] Frontend actualizado con rutas correctas
- [ ] Migraciones creadas
- [ ] Migraciones aplicadas
- [ ] Servidor funcionando

---

**Estado:** ✅ Apps instaladas correctamente
