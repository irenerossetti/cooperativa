"""
Motor del chatbot con respuestas inteligentes
"""
import re
from datetime import datetime


def extract_info(message, conversation):
    """Extrae información del mensaje del usuario"""
    message_lower = message.lower()
    
    # Extraer nombre
    if not conversation.nombre:
        nombre_patterns = [
            r'me llamo ([a-záéíóúñ\s]+)',
            r'soy ([a-záéíóúñ\s]+)',
            r'mi nombre es ([a-záéíóúñ\s]+)',
        ]
        for pattern in nombre_patterns:
            match = re.search(pattern, message_lower)
            if match:
                conversation.nombre = match.group(1).strip().title()
                break
    
    # Extraer edad
    if not conversation.edad:
        edad_patterns = [
            r'tengo (\d+) años',
            r'(\d+) años',
        ]
        for pattern in edad_patterns:
            match = re.search(pattern, message_lower)
            if match:
                conversation.edad = int(match.group(1))
                break
    
    # Detectar tipo de cultivo
    cultivos = ['maíz', 'maiz', 'soja', 'trigo', 'papa', 'tomate', 'cebolla', 'lechuga']
    for cultivo in cultivos:
        if cultivo in message_lower:
            conversation.tipo_cultivo = cultivo
            break
    
    # Detectar necesidad principal
    if 'crédito' in message_lower or 'préstamo' in message_lower or 'financiamiento' in message_lower:
        conversation.necesidad_principal = 'credito'
    elif 'semilla' in message_lower:
        conversation.necesidad_principal = 'semillas'
    elif 'asesor' in message_lower or 'ayuda técnica' in message_lower:
        conversation.necesidad_principal = 'asesoria'
    elif 'afiliar' in message_lower or 'socio' in message_lower:
        conversation.necesidad_principal = 'afiliacion'
    elif 'vender' in message_lower or 'comercializar' in message_lower:
        conversation.necesidad_principal = 'comercializacion'
    
    conversation.save()


def generate_response(message, conversation):
    """Genera una respuesta basada en el mensaje y el contexto"""
    message_lower = message.lower()
    
    # Saludos
    if any(word in message_lower for word in ['hola', 'buenos días', 'buenas tardes', 'buenas noches']):
        if conversation.nombre:
            return f"¡Hola {conversation.nombre}! ¿En qué más puedo ayudarte hoy?"
        return "¡Hola! Bienvenido a la Cooperativa Agrícola. Soy tu asistente virtual. ¿Podrías decirme tu nombre para personalizar nuestra conversación?"
    
    # Presentación
    if conversation.nombre and not conversation.edad:
        return f"Mucho gusto, {conversation.nombre}. Para poder ofrecerte mejor asesoría, ¿podrías decirme tu edad y qué tipo de cultivo tienes?"
    
    # Información sobre créditos
    if 'crédito' in message_lower or 'préstamo' in message_lower or 'financiamiento' in message_lower:
        conversation.fase = 'recomendacion'
        conversation.save()
        return """🏦 **Créditos Agrícolas Disponibles:**

Ofrecemos diferentes líneas de crédito:

1. **Crédito para Insumos** (hasta $50,000)
   - Tasa: 12% anual
   - Plazo: 6-12 meses
   - Para compra de semillas, fertilizantes, pesticidas

2. **Crédito para Maquinaria** (hasta $200,000)
   - Tasa: 15% anual
   - Plazo: hasta 36 meses
   - Para equipamiento agrícola

3. **Crédito de Campaña** (hasta $100,000)
   - Tasa: 10% anual
   - Plazo: según ciclo del cultivo

**Requisitos:**
- Ser socio de la cooperativa
- Tener parcela registrada
- Presentar plan de cultivo

¿Te gustaría más información sobre alguna línea específica?"""
    
    # Información sobre semillas
    if 'semilla' in message_lower:
        cultivo_info = ""
        if conversation.tipo_cultivo:
            cultivo_info = f" especialmente para {conversation.tipo_cultivo}"
        
        return f"""🌱 **Semillas Certificadas Disponibles{cultivo_info}:**

Contamos con semillas de alta calidad:

- **Maíz Híbrido**: $450/bolsa (20kg)
- **Soja Certificada**: $380/bolsa (25kg)
- **Trigo Premium**: $320/bolsa (25kg)
- **Papa Semilla**: $850/bolsa (50kg)

**Beneficios:**
✓ Certificación oficial
✓ Alta germinación (>95%)
✓ Resistencia a plagas
✓ Asesoría técnica incluida
✓ Descuentos para socios

¿Qué cantidad necesitas?"""
    
    # Información sobre asesoría
    if 'asesor' in message_lower or 'ayuda' in message_lower or 'técnica' in message_lower:
        return """👨‍🌾 **Asesoría Técnica Agrícola:**

Nuestros ingenieros agrónomos te pueden ayudar con:

1. **Planificación de Cultivos**
   - Selección de variedades
   - Calendario de siembra
   - Rotación de cultivos

2. **Manejo Integrado de Plagas**
   - Identificación de plagas
   - Control biológico
   - Uso responsable de pesticidas

3. **Fertilización**
   - Análisis de suelo
   - Plan de fertilización
   - Nutrición foliar

4. **Riego y Drenaje**
   - Sistemas de riego
   - Programación de riegos
   - Manejo de agua

**Servicio GRATUITO para socios**

¿Sobre qué tema necesitas asesoría?"""
    
    # Información sobre afiliación
    if 'afiliar' in message_lower or 'socio' in message_lower or 'inscribir' in message_lower:
        return """📝 **Afiliación a la Cooperativa:**

**Beneficios de ser socio:**
✓ Acceso a créditos preferenciales
✓ Descuentos en insumos (10-20%)
✓ Asesoría técnica gratuita
✓ Comercialización de productos
✓ Capacitaciones constantes
✓ Seguro agrícola

**Requisitos:**
- Ser mayor de 18 años
- Tener actividad agrícola
- Copia de DNI
- Constancia de domicilio
- Título o contrato de parcela

**Cuota de inscripción:** $500 (pago único)
**Cuota mensual:** $50

¿Te gustaría iniciar el proceso de afiliación?"""
    
    # Información sobre productos disponibles
    if '¿qué' in message_lower and ('tienen' in message_lower or 'hay' in message_lower):
        return """📦 **Productos y Servicios Disponibles:**

**Insumos Agrícolas:**
🌱 Semillas certificadas
🧪 Fertilizantes (orgánicos e inorgánicos)
🛡️ Pesticidas y fungicidas
🌿 Productos biológicos

**Servicios:**
💰 Créditos agrícolas
👨‍🌾 Asesoría técnica
📚 Capacitaciones
🚜 Alquiler de maquinaria
📊 Comercialización de cosechas

**Beneficios Adicionales:**
✓ Seguro agrícola
✓ Análisis de suelo
✓ Laboratorio de semillas
✓ Almacenamiento de granos

¿Sobre qué producto o servicio quieres más información?"""
    
    # Agradecimiento
    if 'gracias' in message_lower:
        return "¡De nada! Estoy aquí para ayudarte. Si tienes más preguntas, no dudes en consultarme. ¡Que tengas un excelente día! 🌾"
    
    # Despedida
    if any(word in message_lower for word in ['adiós', 'adios', 'chau', 'hasta luego']):
        return "¡Hasta pronto! Que tengas una excelente cosecha. Recuerda que estoy aquí cuando me necesites. 🌾👋"
    
    # Respuesta por defecto
    if conversation.nombre:
        return f"Entiendo, {conversation.nombre}. Puedo ayudarte con información sobre:\n\n• Créditos agrícolas\n• Semillas certificadas\n• Asesoría técnica\n• Afiliación a la cooperativa\n• Comercialización de productos\n\n¿Sobre qué tema te gustaría saber más?"
    else:
        return "Puedo ayudarte con información sobre créditos, semillas, asesoría técnica y más. ¿Podrías decirme tu nombre para comenzar?"


def process_message(message, conversation):
    """Procesa el mensaje y genera una respuesta"""
    # Extraer información del mensaje
    extract_info(message, conversation)
    
    # Intentar usar IA primero
    try:
        from .ai_engine import get_ai_response_with_context
        import os
        
        # Solo usar IA si hay API key configurada (OpenRouter)
        api_key = os.getenv('OPENROUTER_API_KEY')
        print(f"🔑 API Key encontrada: {'Sí' if api_key else 'No'}")
        
        if api_key:
            print(f"🤖 Llamando a OpenRouter para: {message[:50]}...")
            ai_response = get_ai_response_with_context(message, conversation)
            
            if ai_response:
                print(f"✅ Respuesta de IA recibida: {ai_response[:100]}...")
                # Actualizar fase si es necesario
                if conversation.necesidad_principal and conversation.fase == 'exploracion':
                    conversation.fase = 'recomendacion'
                    conversation.save()
                return ai_response
            else:
                print("❌ OpenRouter no devolvió respuesta, usando fallback")
        else:
            print("⚠️ No hay API key, usando respuestas predefinidas")
    except Exception as e:
        print(f"❌ Error al usar IA, usando respuestas predefinidas: {e}")
        import traceback
        traceback.print_exc()
    
    # Fallback a respuestas predefinidas si IA no está disponible
    response = generate_response(message, conversation)
    
    # Actualizar fase si es necesario
    if conversation.necesidad_principal and conversation.fase == 'exploracion':
        conversation.fase = 'recomendacion'
        conversation.save()
    
    return response
