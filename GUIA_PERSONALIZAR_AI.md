# 🤖 GUÍA PARA PERSONALIZAR EL ASISTENTE IA

## Configuración Actual

### API Key Configurada
La API key de OpenRouter está en el archivo `.env`:
```properties
OPENROUTER_API_KEY=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
```

### Modelo Utilizado
```python
model = 'meta-llama/llama-3.1-8b-instruct:free'  # Modelo gratuito
```

---

## Cómo Personalizar las Respuestas

### 1. Modificar el Mensaje del Sistema

**Archivo:** `cooperativa/ai_chat/ai_service.py`

El mensaje del sistema define cómo se comporta la IA. Puedes modificarlo en el método `_build_system_message()`:

```python
def _build_system_message(self, context):
    """
    Construye el mensaje de sistema con contexto
    """
    base_message = """Eres un asistente inteligente para un sistema de gestión de cooperativa agrícola.
Tu objetivo es ayudar a los usuarios a entender y gestionar mejor su cooperativa.

Responde de manera:
- Concisa y clara
- En español
- Con datos específicos cuando estén disponibles
- Sugiriendo acciones cuando sea apropiado

"""
```

#### Ejemplos de Personalización:

**Para un asistente más formal:**
```python
base_message = """Soy el asistente virtual de la cooperativa agrícola.
Mi función es proporcionar información precisa y asistencia profesional 
en la gestión de operaciones cooperativas.

Características de mis respuestas:
- Profesionales y formales
- Basadas en datos verificados
- Con recomendaciones fundamentadas
- En español formal
"""
```

**Para un asistente más amigable:**
```python
base_message = """¡Hola! Soy tu asistente virtual de la cooperativa 😊
Estoy aquí para ayudarte con cualquier pregunta sobre tu cooperativa.

Me gusta:
- Ser claro y directo
- Usar ejemplos prácticos
- Darte consejos útiles
- Hablar en un tono amigable y cercano
"""
```

**Para un asistente especializado en agricultura:**
```python
base_message = """Soy un asistente especializado en gestión agrícola cooperativa.
Tengo conocimientos en:
- Producción agrícola y cultivos
- Gestión de parcelas y recursos
- Comercialización de productos
- Administración cooperativa
- Buenas prácticas agrícolas

Mis respuestas incluyen:
- Datos técnicos cuando sea relevante
- Recomendaciones basadas en mejores prácticas
- Información contextualizada a tu cooperativa
"""
```

---

### 2. Agregar Conocimiento Específico

Puedes agregar información específica sobre tu cooperativa al mensaje del sistema:

```python
base_message += """

**Información sobre nuestra cooperativa:**
- Ubicación: Santa Cruz, Bolivia
- Cultivos principales: Café, Quinua, Cacao
- Número de socios: Aproximadamente 150
- Superficie total: 500 hectáreas
- Fundada en: 2010

**Servicios que ofrecemos:**
- Asistencia técnica agrícola
- Comercialización conjunta
- Acceso a insumos
- Capacitación continua
- Certificaciones orgánicas
"""
```

---

### 3. Mejorar Respuestas Fallback

**Archivo:** `cooperativa/ai_chat/ai_service.py`

Método `_fallback_response()` - Se usa cuando la API de OpenRouter no está disponible:

```python
def _fallback_response(self, message, context):
    """
    Respuesta de fallback cuando la API falla
    """
    message_lower = message.lower()
    
    # Agregar más respuestas predefinidas
    if 'precio' in message_lower or 'cuánto cuesta' in message_lower:
        return {
            'content': 'Para información sobre precios, por favor contacta con el área de ventas o consulta el catálogo de productos.',
            'tokens_used': 0,
            'model': 'fallback'
        }
    
    if 'clima' in message_lower or 'tiempo' in message_lower:
        return {
            'content': 'Puedes consultar el pronóstico del tiempo en la sección de Clima del sistema.',
            'tokens_used': 0,
            'model': 'fallback'
        }
    
    # ... más respuestas ...
```

---

### 4. Ajustar Parámetros del Modelo

**Archivo:** `cooperativa/ai_chat/ai_service.py`

En el método `chat()`, puedes ajustar:

```python
response = requests.post(
    self.api_url,
    headers={
        'Authorization': f'Bearer {self.api_key}',
        'Content-Type': 'application/json',
    },
    json={
        'model': self.model,
        'messages': messages,
        'temperature': 0.7,      # 0.0 = más preciso, 1.0 = más creativo
        'max_tokens': 500,       # Longitud máxima de respuesta
        'top_p': 0.9,           # Diversidad de respuestas
        'frequency_penalty': 0,  # Penalización por repetición
        'presence_penalty': 0,   # Penalización por temas repetidos
    }
)
```

#### Parámetros Explicados:

- **temperature** (0.0 - 1.0):
  - `0.0-0.3`: Respuestas muy precisas y consistentes
  - `0.4-0.7`: Balance entre precisión y creatividad (recomendado)
  - `0.8-1.0`: Respuestas más creativas y variadas

- **max_tokens**:
  - `100-300`: Respuestas cortas
  - `300-500`: Respuestas medianas (recomendado)
  - `500-1000`: Respuestas largas y detalladas

- **top_p** (0.0 - 1.0):
  - `0.9`: Buena diversidad (recomendado)
  - `1.0`: Máxima diversidad

---

### 5. Cambiar el Modelo de IA

Puedes usar diferentes modelos de OpenRouter:

```python
# Modelos gratuitos
self.model = 'meta-llama/llama-3.1-8b-instruct:free'  # Actual
self.model = 'google/gemma-2-9b-it:free'
self.model = 'mistralai/mistral-7b-instruct:free'

# Modelos de pago (mejores respuestas)
self.model = 'anthropic/claude-3-sonnet'
self.model = 'openai/gpt-4-turbo'
self.model = 'google/gemini-pro'
```

**Nota:** Los modelos de pago requieren créditos en OpenRouter.

---

### 6. Agregar Contexto Personalizado

**Archivo:** `cooperativa/ai_chat/views.py`

Método `_get_system_context()` - Agrega más información:

```python
# Agregar información de clima
try:
    from weather.weather_service import WeatherService
    weather_service = WeatherService()
    weather = weather_service.get_current_weather(-17.78, -63.18)
    
    context['weather'] = {
        'temperature': weather.get('main', {}).get('temp'),
        'description': weather.get('weather', [{}])[0].get('description')
    }
except Exception as e:
    print(f"Error obteniendo clima: {e}")

# Agregar alertas activas
try:
    from alerts.models import Alert
    context['alerts'] = {
        'active': Alert.objects.filter(
            is_active=True,
            resolved=False
        ).count()
    }
except Exception as e:
    print(f"Error obteniendo alertas: {e}")
```

---

## Ejemplos de Uso

### Preguntas que el Asistente Puede Responder:

**Información General:**
- "¿Cuántos socios tengo?"
- "¿Cuál es la superficie total de mis parcelas?"
- "¿Cuántas campañas activas hay?"

**Ventas y Finanzas:**
- "¿Cuánto vendí hoy?"
- "¿Cuánto vendí este mes?"
- "¿Cuál es mi mejor producto?"

**Inventario:**
- "¿Qué productos tienen stock bajo?"
- "¿Cuántos items tengo en inventario?"

**Producción:**
- "¿Cuál es mi mejor parcela?"
- "¿Qué cultivos tengo?"

**Recomendaciones:**
- "¿Qué debo hacer hoy?"
- "¿Qué tareas tengo pendientes?"
- "Dame consejos para mejorar mi producción"

---

## Testing

### Probar Diferentes Configuraciones:

1. **Modificar el mensaje del sistema**
2. **Reiniciar el servidor:**
   ```bash
   python manage.py runserver
   ```
3. **Probar en el frontend**
4. **Ajustar según resultados**

### Monitorear Respuestas:

Los logs del servidor mostrarán:
- Errores si los hay
- Tokens utilizados
- Modelo usado
- Tiempo de respuesta

---

## Mejores Prácticas

### 1. Mensaje del Sistema
- ✅ Sé específico sobre el rol del asistente
- ✅ Define el tono de las respuestas
- ✅ Incluye contexto relevante
- ❌ No hagas el mensaje muy largo (máx 500 palabras)

### 2. Contexto
- ✅ Incluye solo datos relevantes
- ✅ Formatea los números claramente
- ✅ Usa unidades (Bs, kg, hectáreas)
- ❌ No sobrecargues con demasiada información

### 3. Parámetros
- ✅ Usa temperature 0.5-0.7 para balance
- ✅ Limita max_tokens a 500-800
- ✅ Mantén top_p en 0.9
- ❌ No uses temperature muy alta (>0.9)

### 4. Fallback
- ✅ Siempre ten respuestas de fallback
- ✅ Usa datos del contexto cuando estén disponibles
- ✅ Sé honesto si no sabes algo
- ❌ No inventes información

---

## Solución de Problemas

### "El servicio de IA no está configurado"
- Verificar que `OPENROUTER_API_KEY` esté en `.env`
- Verificar que esté en `settings.py`
- Reiniciar el servidor

### Respuestas Lentas
- Reducir `max_tokens`
- Usar un modelo más rápido
- Reducir el contexto enviado

### Respuestas Irrelevantes
- Ajustar el mensaje del sistema
- Reducir `temperature`
- Mejorar el contexto

### Errores de API
- Verificar créditos en OpenRouter
- Verificar que la API key sea válida
- Revisar logs del servidor

---

## Recursos Adicionales

- **OpenRouter Docs:** https://openrouter.ai/docs
- **Modelos Disponibles:** https://openrouter.ai/models
- **Precios:** https://openrouter.ai/pricing

---

**Última actualización:** 8 de Diciembre de 2025
