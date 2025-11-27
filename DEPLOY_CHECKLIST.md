# ✅ Checklist de Deploy - Paso a Paso

## Antes de empezar

- [ ] Tienes cuenta en Render (https://render.com)
- [ ] Tienes cuenta en Vercel (https://vercel.com)
- [ ] Tu base de datos Neon está activa
- [ ] Tienes los repositorios en GitHub

## Paso 1: Subir cambios a GitHub

```bash
# Backend
cd Backend
git add .
git commit -m "Preparar para deploy en Render"
git push origin main

# Frontend  
cd ../Frontend
git add .
git commit -m "Preparar para deploy en Vercel"
git push origin main
```

- [ ] Backend pusheado a GitHub
- [ ] Frontend pusheado a GitHub

## Paso 2: Deploy Backend en Render

### 2.1 Crear Web Service
- [ ] Ir a https://dashboard.render.com
- [ ] Click "New +" → "Web Service"
- [ ] Seleccionar repo: `irenerossetti/cooperativa`
- [ ] Click "Connect"

### 2.2 Configuración
```
Name: cooperativa-backend
Environment: Python 3
Build Command: ./build.sh
Start Command: gunicorn config.wsgi:application
```

- [ ] Configuración completada

### 2.3 Variables de Entorno

Copia estas variables (reemplaza con tus valores reales):

```
DATABASE_URL=postgresql://usuario:password@host/database
SECRET_KEY=tu-secret-key-aqui
DEBUG=False
OPENROUTER_API_KEY=tu-api-key (opcional)
OPENWEATHER_API_KEY=tu-api-key (opcional)
```

- [ ] DATABASE_URL agregada
- [ ] SECRET_KEY agregada
- [ ] DEBUG=False configurado
- [ ] APIs opcionales agregadas (si las tienes)

### 2.4 Deploy
- [ ] Click "Create Web Service"
- [ ] Esperar ~5 minutos
- [ ] Verificar que el deploy fue exitoso (verde)
- [ ] Copiar URL: `https://cooperativa-backend.onrender.com`

**Tu URL del backend:** ___________________________________

## Paso 3: Deploy Frontend en Vercel

### 3.1 Crear Proyecto
- [ ] Ir a https://vercel.com
- [ ] Click "Add New..." → "Project"
- [ ] Importar repo: `irenerossetti/cooperativa_frontend`
- [ ] Click "Import"

### 3.2 Configuración
Vercel detecta automáticamente:
```
Framework: Vite
Build Command: npm run build
Output Directory: dist
```

- [ ] Configuración auto-detectada correctamente

### 3.3 Variables de Entorno

Agregar esta variable (usa la URL del backend del Paso 2.4):

```
VITE_API_URL=https://cooperativa-backend.onrender.com
```

- [ ] VITE_API_URL agregada con la URL correcta

### 3.4 Deploy
- [ ] Click "Deploy"
- [ ] Esperar ~2 minutos
- [ ] Verificar que el deploy fue exitoso
- [ ] Copiar URL: `https://tu-proyecto.vercel.app`

**Tu URL del frontend:** ___________________________________

## Paso 4: Configurar CORS

### 4.1 Actualizar Backend
- [ ] Ir a Render → tu servicio backend
- [ ] Click "Environment" en el menú lateral
- [ ] Click "Add Environment Variable"
- [ ] Agregar:
  ```
  Key: CORS_ALLOWED_ORIGINS
  Value: https://tu-proyecto.vercel.app
  ```
  (Usa la URL del Paso 3.4, SIN barra final)
- [ ] Click "Save Changes"
- [ ] Esperar que se redespliegue (~2 minutos)

## Paso 5: Verificar Conexión

### 5.1 Probar Backend
- [ ] Abrir: `https://cooperativa-backend.onrender.com/admin/`
- [ ] Debe cargar la página de admin de Django

### 5.2 Probar Frontend
- [ ] Abrir: `https://tu-proyecto.vercel.app`
- [ ] Debe cargar el landing page
- [ ] Abrir DevTools (F12) → Network
- [ ] Intentar hacer login o navegar
- [ ] Verificar que las peticiones van al backend correcto
- [ ] No debe haber errores CORS

## Paso 6: Crear Datos Iniciales

### 6.1 Acceder al Shell de Render
- [ ] Ir a Render → tu servicio backend
- [ ] Click "Shell" en el menú superior
- [ ] Esperar a que cargue el terminal

### 6.2 Crear Superusuario
```bash
python manage.py createsuperuser
```
- [ ] Superusuario creado
- [ ] Anotar credenciales:
  - Username: _______________
  - Email: _______________
  - Password: _______________

### 6.3 Crear Datos de Prueba (Opcional)
```bash
python create_test_organizations.py
python create_catalog_products.py
python create_community_data.py
```
- [ ] Organizaciones de prueba creadas
- [ ] Productos creados
- [ ] Datos de comunidad creados

## Paso 7: Prueba Final

### 7.1 Login
- [ ] Ir al frontend
- [ ] Click "Iniciar Sesión"
- [ ] Usar credenciales del superusuario
- [ ] Login exitoso

### 7.2 Funcionalidades Clave
- [ ] Dashboard carga correctamente
- [ ] Puedes ver socios/parcelas
- [ ] Reportes funcionan
- [ ] Chatbot responde (si configuraste OPENROUTER_API_KEY)
- [ ] Clima funciona (si configuraste OPENWEATHER_API_KEY)

## 🎉 ¡Deploy Completado!

**URLs Finales:**
- Frontend: ___________________________________
- Backend: ___________________________________
- Admin: ___________________________________/admin/

## 📝 Notas Post-Deploy

### Para la presentación:
- [ ] Crear usuario de demo
- [ ] Preparar datos de ejemplo
- [ ] Probar flujo completo
- [ ] Verificar que todo funciona

### Si algo falla:
1. Revisa los logs en Render (Logs tab)
2. Verifica las variables de entorno
3. Asegúrate de que la BD Neon está activa
4. Espera 30 segundos si el backend está "dormido"

### Mejoras futuras (opcional):
- [ ] Configurar dominio personalizado
- [ ] Habilitar auto-deploy desde GitHub
- [ ] Configurar alertas de errores
- [ ] Upgrade a plan pagado si es necesario

---

**Tiempo total estimado: 15-20 minutos** ⏱️

¡Éxito con tu presentación! 🚀
