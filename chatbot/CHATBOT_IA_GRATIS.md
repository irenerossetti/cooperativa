# 🤖 Chatbot con IA GRATIS usando OpenRouter

## ✅ Implementación Completada

Tu chatbot ahora usa **OpenRouter** con el modelo **Llama 3.1 8B** que es:
- ✅ **100% GRATIS**
- ✅ **Muy inteligente** (comparable a GPT-3.5)
- ✅ **Conversacional natural**
- ✅ **Especializado en agricultura**

## 🚀 Cómo Funciona

### 1. Motor de IA (`ai_engine.py`)
- Usa OpenRouter API
- Modelo: `meta-llama/llama-3.1-8b-instruct:free`
- Mantiene contexto de conversación (últimos 10 mensajes)
- Prompt especializado en cooperativa agrícola

### 2. Fallback Inteligente
Si OpenRouter falla o no está disponible:
- ✅ Usa respuestas predefinidas automáticamente
- ✅ No se rompe el chatbot
- ✅ Sigue funcionando

### 3. Contexto Personalizado
El chatbot recuerda:
- 👤 Nombre del usuario
- 🎂 Edad
- 🌾 Tipo de cultivo
- 💡 Necesidad principal

## 📊 Información que Maneja

### Créditos Agrícolas
- Crédito para Insumos (hasta $50,000)
- Crédito para Maquinaria (hasta $200,000)
- Crédito de Campaña (hasta $100,000)

### Semillas Certificadas
- Maíz Híbrido: $450/bolsa
- Soja Certificada: $380/bolsa
- Trigo Premium: $320/bolsa
- Papa Semilla: $850/bolsa

### Servicios
- Asesoría técnica
- Afiliación
- Comercialización

## 🔧 Configuración

### Tu API Key (Ya configurada)
```env
OPENROUTER_API_KEY=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
```

### Modelo Usado
```python
model = "meta-llama/llama-3.1-8b-instruct:free"
```

## 🧪 Cómo Probar

1. **Abre el chatbot** (botón verde flotante)
2. **Escribe mensajes naturales:**
   - "Hola, me llamo Juan y tengo 35 años"
   - "Cultivo maíz y necesito un crédito"
   - "¿Qué semillas me recomiendan para mi parcela?"
   - "Explícame cómo funciona el crédito de campaña"

3. **Observa las respuestas:**
   - ✅ Naturales y conversacionales
   - ✅ Contextuales (recuerda lo que dijiste)
   - ✅ Específicas para agricultura

## 💡 Ventajas de OpenRouter

### vs OpenAI (GPT)
- ✅ **GRATIS** (OpenAI cobra)
- ✅ Múltiples modelos disponibles
- ✅ Sin límite de uso para modelos gratuitos
- ❌ Ligeramente menos preciso que GPT-4

### vs Ollama (Local)
- ✅ No necesitas GPU
- ✅ No consume recursos de tu servidor
- ✅ Más rápido
- ❌ Requiere internet

## 🔄 Modelos Alternativos GRATIS

Si quieres cambiar el modelo, edita `ai_engine.py`:

```python
# Opciones GRATIS en OpenRouter:

# Llama 3.1 8B (Actual - Recomendado)
"model": "meta-llama/llama-3.1-8b-instruct:free"

# Llama 3.1 70B (Más inteligente pero más lento)
"model": "meta-llama/llama-3.1-70b-instruct:free"

# Mistral 7B (Muy rápido)
"model": "mistralai/mistral-7b-instruct:free"

# Gemma 2 9B (De Google)
"model": "google/gemma-2-9b-it:free"
```

## 📈 Mejoras Futuras

### Fáciles de Implementar:
- [ ] Agregar más información de productos
- [ ] Integrar con base de datos real
- [ ] Consultar disponibilidad de stock
- [ ] Generar cotizaciones automáticas

### Avanzadas:
- [ ] Análisis de sentimientos
- [ ] Recomendaciones personalizadas
- [ ] Integración con WhatsApp
- [ ] Soporte multiidioma (Quechua, Guaraní)

## 🐛 Solución de Problemas

### El chatbot no responde con IA
1. Verifica que `OPENROUTER_API_KEY` esté en `.env`
2. Reinicia el servidor Django
3. Revisa la consola del backend para errores

### Respuestas muy lentas
- Cambia a un modelo más rápido (Mistral 7B)
- Reduce `max_tokens` en `ai_engine.py`

### Respuestas no relacionadas con agricultura
- El prompt del sistema está optimizado
- Si persiste, ajusta `SYSTEM_PROMPT` en `ai_engine.py`

## 📊 Comparación de Costos

| Servicio | Costo | Calidad | Velocidad |
|----------|-------|---------|-----------|
| **OpenRouter (Llama 3.1)** | **GRATIS** | ⭐⭐⭐⭐ | ⚡⚡⚡ |
| OpenAI GPT-3.5 | $0.002/1K tokens | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ |
| OpenAI GPT-4 | $0.03/1K tokens | ⭐⭐⭐⭐⭐ | ⚡⚡ |
| Anthropic Claude | $0.008/1K tokens | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ |
| Ollama (Local) | GRATIS | ⭐⭐⭐⭐ | ⚡⚡ |

## ✅ Estado Actual

**Chatbot con IA: 100% Funcional** 🎉
- OpenRouter integrado ✅
- Modelo Llama 3.1 8B ✅
- Respuestas naturales ✅
- Contexto de conversación ✅
- Fallback a respuestas predefinidas ✅
- 100% GRATIS ✅

¡Tu chatbot ahora es tan inteligente como ChatGPT pero GRATIS! 🚀
