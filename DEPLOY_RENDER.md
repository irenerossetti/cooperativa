# Guía de Deploy en Render

## Archivos preparados para deploy ✅

- `requirements.txt` - Actualizado con gunicorn y whitenoise
- `build.sh` - Script de build para Render
- `render.yaml` - Configuración de Render
- `settings.py` - Configurado para producción

## Pasos para Deploy en Render

### 1. Preparar el repositorio

Asegúrate de hacer commit y push de todos los cambios:

```bash
cd Backend
git add .
git commit -m "Preparar para deploy en Render"
git push origin main
```

### 2. Crear Web Service en Render

1. Ve a https://dashboard.render.com
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio: `irenerossetti/cooperativa`
4. Configuración:
   - **Name**: `cooperativa-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`
   - **Instance Type**: `Free`

### 3. Configurar Variables de Entorno

En la sección "Environment" de Render, agrega:

**Obligatorias:**
- `DATABASE_URL` - Tu URL de Neon (cópiala de tu .env)
- `SECRET_KEY` - Genera una nueva o usa la de tu .env
- `DEBUG` - `False`

**Opcionales (para funcionalidades completas):**
- `OPENROUTER_API_KEY` - Para el chatbot con IA
- `OPENWEATHER_API_KEY` - Para predicciones climáticas
- `CORS_ALLOWED_ORIGINS` - URLs del frontend separadas por comas

Ejemplo de `CORS_ALLOWED_ORIGINS`:
```
https://tu-frontend.vercel.app,https://www.tu-dominio.com
```

### 4. Deploy

1. Click en "Create Web Service"
2. Render automáticamente:
   - Clonará tu repo
   - Instalará dependencias
   - Ejecutará migraciones
   - Iniciará el servidor

### 5. Verificar el Deploy

Una vez completado, tu backend estará en:
```
https://cooperativa-backend.onrender.com
```

Prueba los endpoints:
- `https://cooperativa-backend.onrender.com/api/health/` (si existe)
- `https://cooperativa-backend.onrender.com/admin/`

### 6. Configurar Frontend

Actualiza la variable de entorno en tu frontend:
```
VITE_API_URL=https://cooperativa-backend.onrender.com
```

## Comandos útiles después del deploy

### Crear superusuario
En el Shell de Render:
```bash
python manage.py createsuperuser
```

### Ver logs
En el dashboard de Render → Logs

### Ejecutar migraciones manualmente
```bash
python manage.py migrate
```

### Crear datos de prueba
```bash
python create_test_organizations.py
python create_superuser.py
```

## Troubleshooting

### Error: "Application failed to respond"
- Verifica que `gunicorn` esté en requirements.txt
- Revisa los logs en Render

### Error: "Database connection failed"
- Verifica que `DATABASE_URL` esté correctamente configurada
- Asegúrate de que Neon esté activo

### Error: "Static files not found"
- Verifica que `whitenoise` esté instalado
- Ejecuta `python manage.py collectstatic`

### CORS errors
- Agrega la URL del frontend a `CORS_ALLOWED_ORIGINS`
- O temporalmente usa `CORS_ALLOW_ALL_ORIGINS=True`

## Notas importantes

⚠️ **Render Free Tier:**
- El servicio se "duerme" después de 15 minutos de inactividad
- Primera petición después de dormir toma ~30 segundos
- Suficiente para demos y desarrollo

💡 **Recomendaciones:**
- Usa el plan Starter ($7/mes) para producción real
- Configura un dominio personalizado
- Habilita auto-deploy desde GitHub

## Próximos pasos

1. ✅ Deploy del backend en Render
2. 🔄 Deploy del frontend en Vercel
3. 🔄 Conectar frontend con backend
4. 🔄 Crear datos de prueba en producción
