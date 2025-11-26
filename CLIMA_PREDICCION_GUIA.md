# 🌤️ Sistema de Predicción del Clima

## 📊 Comparación de APIs

| API | Llamadas Gratis | Precisión | Facilidad |
|-----|----------------|-----------|-----------|
| **OpenWeatherMap** | 1,000/día | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **AccuWeather** | 50/día | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **WeatherAPI** | 1M/mes | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎯 Recomendación: OpenWeatherMap

### ¿Por qué OpenWeatherMap?
- ✅ 1,000 llamadas gratis al día (vs 50 de AccuWeather)
- ✅ Ya está configurado en tu proyecto
- ✅ API muy simple de usar
- ✅ Datos precisos para agricultura
- ✅ Pronóstico de 5 días incluido

## 🚀 Implementación

### 1. Obtener API Key (GRATIS)

1. Ve a: https://openweathermap.org/api
2. Crea una cuenta gratis
3. Ve a "API keys"
4. Copia tu API key
5. Agrégala al `.env`:
   ```
   OPENWEATHER_API_KEY=tu_api_key_aqui
   ```

### 2. Datos que Obtendrás

**Clima Actual:**
- 🌡️ Temperatura actual
- 💧 Humedad
- 🌧️ Probabilidad de lluvia
- 💨 Velocidad del viento
- ☁️ Nubosidad
- 🌅 Amanecer/Atardecer

**Pronóstico 5 Días:**
- Temperatura máxima/mínima
- Condiciones del clima
- Probabilidad de precipitación
- Velocidad del viento

**Datos Agrícolas Específicos:**
- Índice UV
- Punto de rocío
- Presión atmosférica
- Visibilidad

### 3. Endpoints que Crearemos

```
GET /api/weather/current/?lat=-17.78&lon=-63.18
GET /api/weather/forecast/?lat=-17.78&lon=-63.18
GET /api/weather/agricultural/?lat=-17.78&lon=-63.18
```

### 4. Casos de Uso Agrícolas

**Alertas Automáticas:**
- 🌧️ "Lluvia en las próximas 24h - Posponer fumigación"
- ☀️ "3 días de sol - Ideal para cosecha"
- 🌡️ "Helada prevista - Proteger cultivos"
- 💨 "Vientos fuertes - No aplicar pesticidas"

**Recomendaciones:**
- Mejor momento para sembrar
- Cuándo regar (basado en lluvia prevista)
- Cuándo aplicar fertilizantes
- Alertas de plagas (basado en humedad/temperatura)

## 📱 Interfaz que Crearemos

### Widget de Clima en Dashboard
```
┌─────────────────────────────┐
│  🌤️ Clima Actual            │
│  Santa Cruz, Bolivia        │
│                             │
│  🌡️ 28°C  💧 65%           │
│  Parcialmente nublado       │
│                             │
│  Pronóstico 5 días:         │
│  Lun: ☀️ 30°C              │
│  Mar: 🌧️ 25°C              │
│  Mié: ⛅ 27°C              │
│  Jue: ☀️ 29°C              │
│  Vie: 🌤️ 28°C              │
│                             │
│  ⚠️ Alerta: Lluvia mañana  │
└─────────────────────────────┘
```

### Página Completa de Clima
- Mapa interactivo
- Gráficos de temperatura
- Historial de clima
- Alertas personalizadas por parcela

## 🔄 Alternativa: AccuWeather

Si prefieres AccuWeather:

### Ventajas:
- Más preciso (especialmente para agricultura)
- Datos más detallados
- Mejor para pronósticos a largo plazo

### Desventajas:
- Solo 50 llamadas/día gratis
- Proceso de aprobación más lento
- API más compleja

### Cómo Obtener API Key:
1. Ve a: https://developer.accuweather.com/
2. Crea cuenta
3. Solicita API key (tarda 1-2 días en aprobar)
4. Plan gratuito: 50 llamadas/día

## 💡 Recomendación Final

**Para tu proyecto, usa OpenWeatherMap porque:**
1. Es suficiente para agricultura
2. 1,000 llamadas/día es más que suficiente
3. Implementación más rápida
4. Gratis sin límites molestos

**Usa AccuWeather solo si:**
- Necesitas precisión extrema
- Tienes presupuesto ($25/mes para 500 llamadas/día)
- Necesitas pronósticos de 15 días

## 🎯 Próximos Pasos

1. Obtener API key de OpenWeatherMap
2. Implementar backend (weather app)
3. Crear endpoints
4. Diseñar widget de clima
5. Agregar alertas automáticas
6. Integrar con parcelas

¿Quieres que implemente el sistema completo con OpenWeatherMap?
