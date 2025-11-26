# Sistema de Reportes con Inteligencia Artificial

## 🧠 Descripción General

Sistema avanzado de reportes que combina:
- **Random Forest**: Predicción de rendimientos agrícolas
- **Web Speech API**: Reconocimiento de voz para comandos
- **Text-to-Speech**: Respuestas por voz del asistente
- **Machine Learning**: Análisis predictivo de producción

---

## 🎯 Características Implementadas

### 1. **Predicción con Random Forest**

#### Modelo de Machine Learning:
- **Algoritmo**: Random Forest Regressor
- **Objetivo**: Predecir rendimiento (kg/ha) de parcelas
- **Features utilizadas**:
  - Superficie de la parcela (ha)
  - Tipo de suelo (encoded)
  - Tipo de cultivo (encoded)
  - Historial de cosechas

#### Endpoints del Backend:

```python
POST /api/reports/reports/train_ml_model/
# Entrena el modelo con datos históricos
# Respuesta:
{
  "success": true,
  "train_score": 0.95,
  "test_score": 0.87,
  "samples": 150,
  "message": "Modelo entrenado con 150 muestras"
}
```

```python
GET /api/reports/reports/predict_yield/?parcel_id=1
# Predice rendimiento de una parcela específica
# Respuesta:
{
  "parcel_id": 1,
  "parcel_code": "PARC-001",
  "predicted_yield": 85.5,
  "predicted_production": 427.5,
  "historical_avg": 80.0,
  "confidence": "medium",
  "recommendation": "Excelente: Se espera un aumento del 6.9% en el rendimiento"
}
```

```python
GET /api/reports/reports/predict_partner_production/?partner_id=1
# Predice producción total de un socio
# Respuesta:
{
  "partner_id": 1,
  "partner_name": "Juan Pérez",
  "total_predicted_production": 1250.5,
  "parcels_count": 3,
  "parcel_predictions": [...]
}
```

```python
GET /api/reports/reports/ml_insights/
# Obtiene insights del modelo
# Respuesta:
{
  "feature_importance": {
    "surface": 0.45,
    "soil_type": 0.25,
    "crop_type": 0.20,
    "harvest_count": 0.10
  },
  "model_status": "trained"
}
```

---

### 2. **Asistente de Voz**

#### Tecnologías:
- **Web Speech API**: Reconocimiento de voz (Chrome/Edge)
- **Speech Synthesis API**: Respuestas por voz
- **Idioma**: Español (es-ES)

#### Comandos Soportados:

| Comando de Voz | Acción |
|----------------|--------|
| "Muestra producción por parcela" | Navega al reporte de producción |
| "Genera reporte de labores" | Navega al reporte de labores |
| "Predice rendimiento de parcela" | Genera predicción con ML |
| "Exportar en Excel" | Exporta reporte actual |
| "Producción mayor a 100" | Aplica filtro de producción |

#### Extracción de Filtros por Voz:
```javascript
// El asistente puede extraer filtros del comando:
"Muestra producción mayor a 100 kilogramos"
→ { minProduction: 100 }

"Reporte del socio Juan Pérez"
→ { partnerName: "Juan Pérez" }

"Producción menor a 50"
→ { maxProduction: 50 }
```

---

## 📁 Estructura de Archivos

### Backend:
```
Backend/
├── reports/
│   ├── ml_predictions.py          # Lógica de ML
│   ├── views.py                   # Endpoints de API
│   ├── models/                    # Modelos entrenados
│   │   ├── .gitignore
│   │   └── yield_predictor.pkl    # Modelo guardado
│   └── ...
└── requirements.txt               # Dependencias (scikit-learn, numpy, joblib)
```

### Frontend:
```
Frontend/
└── src/
    ├── components/
    │   └── reports/
    │       └── VoiceReportAssistant.jsx  # Asistente de voz
    └── pages/
        └── reports/
            └── ReportesIA.jsx             # Página principal de IA
```

---

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias del Backend:

```bash
cd Backend
pip install -r requirements.txt
```

Esto instalará:
- `scikit-learn>=1.3.0` - Machine Learning
- `numpy>=1.24.0` - Operaciones numéricas
- `joblib>=1.3.0` - Serialización de modelos

### 2. Crear Directorio para Modelos:

```bash
mkdir -p reports/models
```

### 3. Entrenar el Modelo:

Opción A - Desde la interfaz web:
1. Navega a "Reportes con IA"
2. Haz clic en "Entrenar Modelo"
3. Espera a que termine el entrenamiento

Opción B - Desde Python:
```python
from reports.ml_predictions import YieldPredictor

predictor = YieldPredictor()
result = predictor.train()
print(result)
```

### 4. Verificar Navegador Compatible:

El asistente de voz requiere:
- ✅ Google Chrome
- ✅ Microsoft Edge
- ❌ Firefox (no soporta Web Speech API completamente)
- ❌ Safari (soporte limitado)

---

## 💡 Casos de Uso

### Caso 1: Predicción de Rendimiento

**Escenario**: Un agrónomo quiere saber qué rendimiento esperar de una parcela nueva.

**Flujo**:
1. Usuario entrena el modelo con datos históricos
2. Selecciona la parcela en el dropdown
3. Hace clic en "Predecir Rendimiento"
4. Sistema muestra:
   - Rendimiento predicho: 85.5 kg/ha
   - Producción total: 427.5 kg
   - Comparación con promedio histórico
   - Recomendación: "Excelente: Se espera un aumento del 6.9%"

### Caso 2: Comando por Voz

**Escenario**: Usuario quiere generar un reporte sin usar el mouse.

**Flujo**:
1. Usuario hace clic en el micrófono
2. Dice: "Muestra producción por parcela mayor a 100 kilogramos"
3. Sistema:
   - Transcribe el audio
   - Extrae filtros (minProduction: 100)
   - Navega al reporte
   - Aplica filtros automáticamente
   - Responde por voz: "Generando reporte de producción por parcela"

### Caso 3: Análisis de Factores

**Escenario**: Administrador quiere saber qué factores afectan más el rendimiento.

**Flujo**:
1. Usuario entrena el modelo
2. Visualiza "Importancia de Factores"
3. Sistema muestra gráfico:
   - Superficie: 45%
   - Tipo de Suelo: 25%
   - Tipo de Cultivo: 20%
   - Historial: 10%
4. Conclusión: La superficie es el factor más importante

---

## 🔬 Detalles Técnicos del Modelo

### Random Forest Regressor

**Hiperparámetros**:
```python
RandomForestRegressor(
    n_estimators=100,      # 100 árboles de decisión
    max_depth=10,          # Profundidad máxima de 10 niveles
    random_state=42        # Semilla para reproducibilidad
)
```

**Proceso de Entrenamiento**:
1. **Recolección de datos**: Obtiene todas las parcelas con producción histórica
2. **Feature Engineering**: Convierte datos categóricos a numéricos
3. **Split**: 80% entrenamiento, 20% prueba
4. **Entrenamiento**: Ajusta el modelo con datos de entrenamiento
5. **Evaluación**: Calcula R² score en conjunto de prueba
6. **Persistencia**: Guarda modelo en archivo .pkl

**Métricas de Evaluación**:
- **R² Score**: Mide qué tan bien el modelo explica la varianza
  - 1.0 = Predicción perfecta
  - 0.8-0.9 = Muy bueno
  - 0.6-0.8 = Aceptable
  - <0.6 = Necesita mejora

**Limitaciones**:
- Requiere mínimo 10 registros históricos
- Precisión depende de la calidad de datos
- No considera factores externos (clima, plagas, etc.)

---

## 🎤 Detalles del Asistente de Voz

### Web Speech API

**Configuración**:
```javascript
const recognition = new webkitSpeechRecognition();
recognition.continuous = false;      // Una frase a la vez
recognition.interimResults = true;   // Resultados parciales
recognition.lang = 'es-ES';          // Español
```

**Eventos**:
- `onstart`: Cuando empieza a escuchar
- `onresult`: Cuando detecta palabras
- `onend`: Cuando termina de escuchar
- `onerror`: Si hay un error

**Procesamiento de Comandos**:
```javascript
const processCommand = (transcript) => {
  const lower = transcript.toLowerCase();
  
  // Detección de intención
  if (lower.includes('producción') && lower.includes('parcela')) {
    // Navegar a reporte de producción
  }
  
  // Extracción de entidades
  const match = lower.match(/mayor a (\d+)/);
  if (match) {
    filters.minProduction = match[1];
  }
}
```

### Speech Synthesis API

**Configuración**:
```javascript
const utterance = new SpeechSynthesisUtterance(text);
utterance.lang = 'es-ES';
utterance.rate = 1.0;  // Velocidad normal
window.speechSynthesis.speak(utterance);
```

---

## 📊 Ejemplos de Predicciones

### Ejemplo 1: Parcela con Buen Rendimiento

```json
{
  "parcel_code": "PARC-001",
  "predicted_yield": 95.2,
  "predicted_production": 476.0,
  "historical_avg": 88.5,
  "recommendation": "Excelente: Se espera un aumento del 7.6% en el rendimiento"
}
```

### Ejemplo 2: Parcela con Bajo Rendimiento

```json
{
  "parcel_code": "PARC-005",
  "predicted_yield": 62.3,
  "predicted_production": 186.9,
  "historical_avg": 75.0,
  "recommendation": "Alerta: Se espera una disminución significativa del 16.9%"
}
```

---

## 🔧 Troubleshooting

### Problema: "Modelo no entrenado"
**Solución**: Haz clic en "Entrenar Modelo" en la página de Reportes con IA

### Problema: "Datos insuficientes para entrenar"
**Solución**: Necesitas al menos 10 parcelas con producción histórica

### Problema: "Navegador no soporta reconocimiento de voz"
**Solución**: Usa Google Chrome o Microsoft Edge

### Problema: "No se escucha la respuesta por voz"
**Solución**: Verifica que el volumen esté activado y que el navegador tenga permisos de audio

### Problema: "Predicción muy diferente a la realidad"
**Solución**: 
- Entrena el modelo con más datos
- Verifica la calidad de los datos históricos
- Considera factores externos no incluidos en el modelo

---

## 🚀 Mejoras Futuras

### Corto Plazo:
1. **Más Features**: Agregar clima, fertilizantes, plagas
2. **Modelos Específicos**: Un modelo por tipo de cultivo
3. **Intervalos de Confianza**: Mostrar rango de predicción
4. **Validación Cruzada**: Mejor evaluación del modelo

### Mediano Plazo:
1. **Deep Learning**: Usar redes neuronales para mejor precisión
2. **Series Temporales**: Predecir tendencias a lo largo del tiempo
3. **Integración con Dialogflow**: NLP más avanzado
4. **Recomendaciones Automáticas**: Sugerir acciones basadas en predicciones

### Largo Plazo:
1. **Computer Vision**: Análisis de imágenes de cultivos
2. **IoT Integration**: Datos en tiempo real de sensores
3. **Optimización Multi-objetivo**: Maximizar rendimiento y minimizar costos
4. **Federated Learning**: Aprender de múltiples cooperativas sin compartir datos

---

## ✅ Checklist de Implementación

- ✅ Modelo Random Forest implementado
- ✅ Endpoints de API creados
- ✅ Asistente de voz funcional
- ✅ Interfaz de usuario completa
- ✅ Predicciones por parcela
- ✅ Predicciones por socio
- ✅ Insights de importancia de features
- ✅ Comandos de voz en español
- ✅ Respuestas por voz
- ✅ Extracción de filtros por voz
- ✅ Documentación completa

---

## 📚 Referencias

- [Scikit-learn Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [Speech Synthesis API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis)

---

**¡El sistema de reportes con IA está completamente implementado y listo para usar!** 🎉🧠🎤
