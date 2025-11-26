# 🚀 Guía Rápida - Reportes con IA

## ✅ Sistema Instalado y Funcionando

El servidor Django está corriendo en: **http://127.0.0.1:8000/**

---

## 📋 Pasos para Usar el Sistema

### 1. **Acceder a Reportes con IA**

Navega a: `http://localhost:8000/reportes/ia` (necesitarás agregar la ruta en el frontend)

O usa los endpoints directamente:

### 2. **Entrenar el Modelo**

```bash
# Opción A: Desde la interfaz web
# Click en "Entrenar Modelo" en la página de Reportes con IA

# Opción B: Desde la API
curl -X POST http://localhost:8000/api/reports/reports/train_ml_model/ \
  -H "X-Organization-Subdomain: sanjuan"
```

### 3. **Generar Predicciones**

```bash
# Predecir rendimiento de una parcela
curl http://localhost:8000/api/reports/reports/predict_yield/?parcel_id=1 \
  -H "X-Organization-Subdomain: sanjuan"

# Predecir producción de un socio
curl http://localhost:8000/api/reports/reports/predict_partner_production/?partner_id=1 \
  -H "X-Organization-Subdomain: sanjuan"
```

### 4. **Obtener Insights del Modelo**

```bash
curl http://localhost:8000/api/reports/reports/ml_insights/ \
  -H "X-Organization-Subdomain: sanjuan"
```

---

## 🎤 Usar el Asistente de Voz

1. Abre la página de Reportes con IA
2. Haz clic en el botón del micrófono
3. Di uno de estos comandos:
   - "Muestra producción por parcela"
   - "Predice rendimiento de parcela"
   - "Genera reporte de labores"
   - "Exportar en Excel"

---

## 📊 Reportes Dinámicos

### Producción por Parcela:
1. Navega a `/reportes/produccion-parcela`
2. Click en "Columnas" para seleccionar qué mostrar
3. Aplica filtros según necesites
4. Exporta en el formato deseado

### Labores por Campaña:
1. Navega a `/reportes/labores-campana`
2. Click en "Columnas" para personalizar
3. Usa filtros de fecha y rangos numéricos
4. Exporta el reporte

---

## 🔧 Comandos Útiles

### Generar más datos de prueba:
```bash
cd Backend
.\venv\Scripts\python.exe create_production_data.py
```

### Probar el sistema ML:
```bash
.\venv\Scripts\python.exe test_ml_system.py
```

### Reiniciar servidor:
```bash
.\venv\Scripts\python.exe manage.py runserver
```

---

## 📁 Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/reports/reports/train_ml_model/` | POST | Entrena el modelo |
| `/api/reports/reports/predict_yield/` | GET | Predice rendimiento |
| `/api/reports/reports/predict_partner_production/` | GET | Predice producción socio |
| `/api/reports/reports/ml_insights/` | GET | Insights del modelo |
| `/api/reports/reports/performance_by_parcel/` | GET | Reporte por parcela |
| `/api/reports/reports/performance_by_partner/` | GET | Reporte por socio |
| `/api/reports/reports/export_report/` | POST | Exportar reporte |

---

## ⚠️ Notas Importantes

1. **Entorno Virtual**: Siempre usa `.\venv\Scripts\python.exe` para ejecutar comandos
2. **Organización**: Incluye el header `X-Organization-Subdomain: sanjuan` en las peticiones
3. **Datos**: El modelo necesita al menos 10 registros de producción para entrenar
4. **Navegador**: El asistente de voz funciona mejor en Chrome o Edge

---

## 🎯 Próximos Pasos

1. Agregar la ruta `/reportes/ia` en el frontend
2. Probar el asistente de voz
3. Generar más datos históricos para mejor precisión
4. Explorar las predicciones y recomendaciones

---

**¡El sistema está listo para usar!** 🎉🧠🎤
