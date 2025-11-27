# 🚀 Resumen Completo de Deploy

## ✅ Archivos Preparados

### Backend (Django)
- ✅ `requirements.txt` - Actualizado con gunicorn y whitenoise
- ✅ `build.sh` - Script de build para Render (ejecutable)
- ✅ `render.yaml` - Configuración de Render
- ✅ `config/settings.py` - Configurado para producción
- ✅ `DEPLOY_RENDER.md` - Guía detallada

### Frontend (React + Vite)
- ✅ `.env.production` - Variables de entorno para producción
- ✅ `vite.config.js` - Configurado con proxy
- ✅ `DEPLOY_VERCEL.md` - Guía detallada

## 📋 Pasos Rápidos para Deploy

### 1. Subir cambios a GitHub

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

### 2. Deploy Backend en Render

1. Ve a https://dashboard.render.com
2. New + → Web Service
3. Conecta repo: `irenerossetti/cooperativa`
4. Configuración:
   - Name: `cooperativa-backend`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi:application`
5. Variables de entorno:
   ```
   DATABASE_URL=tu_url_de_neon
   SECRET_KEY=tu_secret_key
   DEBUG=False
   OPENROUTER_API_KEY=tu_api_key (opcional)
   OPENWEATHER_API_KEY=tu_api_key (opcional)
   ```
6. Create Web Service
7. Espera ~5 minutos
8. Copia la URL: `https://cooperativa-backend.onrender.com`

### 3. Deploy Frontend en Vercel

1. Ve a https://vercel.com
2. Add New → Project
3. Importa repo: `irenerossetti/cooperativa_frontend`
4. Variables de entorno:
   ```
   VITE_API_URL=https://cooperativa-backend.onrender.com
   ```
5. Deploy
6. Espera ~2 minutos
7. Copia la URL: `https://tu-proyecto.vercel.app`

### 4. Actualizar CORS en Backend

1. Ve a Render → tu servicio backend
2. Environment → Add Environment Variable:
   ```
   CORS_ALLOWED_ORIGINS=https://tu-proyecto.vercel.app
   ```
3. Save Changes (se redesplegará automáticamente)

### 5. Crear Superusuario y Datos de Prueba

En Render → Shell:
```bash
python manage.py createsuperuser
python create_test_organizations.py
python create_superuser.py
```

## 🎯 URLs Finales

- **Frontend**: https://tu-proyecto.vercel.app
- **Backend**: https://cooperativa-backend.onrender.com
- **Admin**: https://cooperativa-backend.onrender.com/admin/

## ✨ Funcionalidades Desplegadas

- ✅ Sistema Multi-Tenant completo
- ✅ Autenticación y roles
- ✅ Gestión de socios, parcelas, campañas
- ✅ Módulo de ventas
- ✅ Reportes dinámicos con exportación
- ✅ Chatbot con IA (OpenRouter)
- ✅ Predicciones climáticas
- ✅ Análisis de mercado
- ✅ Sistema de auditoría
- ✅ Panel de Super Admin
- ✅ Landing page con método de pago
- ✅ Dashboards por rol

## 🔍 Verificación Post-Deploy

### Backend
```bash
# Health check
curl https://cooperativa-backend.onrender.com/admin/

# API check
curl https://cooperativa-backend.onrender.com/api/tenants/organizations/
```

### Frontend
1. Abre https://tu-proyecto.vercel.app
2. Verifica que el landing page carga
3. Intenta hacer login
4. Verifica que las peticiones van al backend correcto (DevTools → Network)

## ⚠️ Notas Importantes

### Render Free Tier
- El servicio se "duerme" después de 15 minutos sin uso
- Primera petición toma ~30 segundos en despertar
- Suficiente para demos y presentaciones

### Vercel Free Tier
- Deploy automático en cada push
- CDN global súper rápido
- Sin límites prácticos para tu uso

### Base de Datos (Neon)
- Ya está configurada
- Asegúrate de que esté activa
- Verifica la conexión desde Render

## 🐛 Troubleshooting Rápido

**Backend no inicia:**
- Revisa logs en Render
- Verifica DATABASE_URL
- Asegúrate de que build.sh es ejecutable

**Frontend no conecta:**
- Verifica VITE_API_URL en Vercel
- Revisa CORS_ALLOWED_ORIGINS en Render
- Espera a que el backend despierte (30s)

**CORS errors:**
- Agrega la URL de Vercel a CORS_ALLOWED_ORIGINS
- Sin barra final: `https://tu-proyecto.vercel.app`

## 📊 Datos de Prueba

Después del deploy, ejecuta en Render Shell:

```bash
# Crear organizaciones de prueba
python create_test_organizations.py

# Crear productos
python create_catalog_products.py

# Crear datos de comunidad
python create_community_data.py

# Crear datos de producción
python create_production_data.py
```

## 🎉 ¡Listo para Presentar!

Tu sistema está completamente desplegado y funcional. Puedes:
- Demostrar el sistema multi-tenant
- Mostrar las funcionalidades de IA
- Presentar los reportes dinámicos
- Demostrar el panel de super admin
- Mostrar el landing page con pago

## 📞 Soporte

Si algo falla:
1. Revisa los logs en Render
2. Verifica las variables de entorno
3. Asegúrate de que la BD está activa
4. Espera 30 segundos si el backend está dormido

---

**Tiempo estimado total de deploy: 10-15 minutos** ⏱️
