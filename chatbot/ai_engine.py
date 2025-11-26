"""
Motor de IA para el chatbot usando OpenRouter (GRATIS)
"""
import os
import urllib.request
import urllib.error
import json

# URL de OpenRouter
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Prompt del sistema para el chatbot agrícola
SYSTEM_PROMPT = """Eres un asistente virtual experto de una Cooperativa Agrícola en Bolivia. 

Tu rol es ayudar a agricultores y socios con:
- Información sobre créditos agrícolas
- Semillas certificadas y productos disponibles
- Asesoría técnica agrícola
- Proceso de afiliación a la cooperativa
- Comercialización de productos
- Servicios de la cooperativa

INFORMACIÓN DE LA COOPERATIVA:

**Créditos Disponibles:**
1. Crédito para Insumos (hasta $50,000) - Tasa: 12% anual - Plazo: 6-12 meses
2. Crédito para Maquinaria (hasta $200,000) - Tasa: 15% anual - Plazo: hasta 36 meses
3. Crédito de Campaña (hasta $100,000) - Tasa: 10% anual - Plazo: según ciclo del cultivo

**Semillas Certificadas:**
- Maíz Híbrido: $450/bolsa (20kg)
- Soja Certificada: $380/bolsa (25kg)
- Trigo Premium: $320/bolsa (25kg)
- Papa Semilla: $850/bolsa (50kg)

**Servicios de Asesoría:**
- Planificación de cultivos
- Manejo integrado de plagas
- Fertilización y análisis de suelo
- Sistemas de riego

**Requisitos para Afiliación:**
- Ser mayor de 18 años
- Tener actividad agrícola
- Documentos: DNI, constancia de domicilio, título de parcela
- Cuota de inscripción: $500 (pago único)
- Cuota mensual: $50

INSTRUCCIONES:
- Sé amable, profesional y empático
- Usa un lenguaje claro y accesible para agricultores
- Haz preguntas para entender mejor las necesidades
- Proporciona información específica y útil
- Si no sabes algo, sé honesto y ofrece alternativas
- Usa emojis ocasionalmente para ser más amigable (🌾 🌱 💰 👨‍🌾)
- Responde en español
"""


def get_ai_response(message, conversation_history=None):
    """
    Obtiene una respuesta de IA usando OpenRouter (GRATIS)
    
    Args:
        message: Mensaje del usuario
        conversation_history: Lista de mensajes previos [{'role': 'user/assistant', 'content': '...'}]
    
    Returns:
        str: Respuesta generada por la IA
    """
    try:
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            print("❌ No se encontró OPENROUTER_API_KEY en variables de entorno")
            return None
        
        print(f"✅ API Key encontrada: {api_key[:20]}...")
        
        # Construir historial de mensajes
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Agregar historial si existe (últimos 10 mensajes)
        if conversation_history:
            messages.extend(conversation_history[-10:])
        
        # Agregar mensaje actual
        messages.append({"role": "user", "content": message})
        
        # Headers para OpenRouter
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",  # Tu sitio
            "X-Title": "Cooperativa Chatbot"
        }
        
        # Payload para OpenRouter
        payload = {
            "model": "mistralai/mistral-7b-instruct:free",  # Modelo GRATIS y muy bueno
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500,
            "top_p": 0.9,
            "frequency_penalty": 0.3,
            "presence_penalty": 0.3
        }
        
        # Llamar a OpenRouter usando urllib
        print(f"📡 Enviando request a OpenRouter...")
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            OPENROUTER_API_URL,
            data=data,
            headers=headers,
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                ai_message = result['choices'][0]['message']['content'].strip()
                print(f"✅ Respuesta de IA: {ai_message[:100]}...")
                return ai_message
                
        except urllib.error.HTTPError as e:
            print(f"❌ Error HTTP de OpenRouter: {e.code}")
            error_body = e.read().decode('utf-8')
            print(f"📄 Response: {error_body[:500]}")
            return None
        except urllib.error.URLError as e:
            print(f"❌ Error de conexión: {e.reason}")
            return None
    
    except Exception as e:
        print(f"Error al obtener respuesta de IA: {e}")
        return None


def get_ai_response_with_context(message, conversation):
    """
    Obtiene respuesta de IA con contexto de la conversación
    
    Args:
        message: Mensaje del usuario
        conversation: Objeto ChatConversation con historial
    
    Returns:
        str: Respuesta generada por la IA
    """
    # Construir historial de conversación
    history = []
    messages = conversation.messages.order_by('timestamp')[:20]  # Últimos 20 mensajes
    
    for msg in messages:
        role = "user" if msg.message_type == "user" else "assistant"
        history.append({"role": role, "content": msg.content})
    
    # Agregar contexto del usuario si está disponible
    context_info = []
    if conversation.nombre:
        context_info.append(f"Nombre del usuario: {conversation.nombre}")
    if conversation.edad:
        context_info.append(f"Edad: {conversation.edad} años")
    if conversation.tipo_cultivo:
        context_info.append(f"Cultivo principal: {conversation.tipo_cultivo}")
    if conversation.necesidad_principal:
        context_info.append(f"Necesidad: {conversation.necesidad_principal}")
    
    # Si hay contexto, agregarlo al mensaje
    if context_info:
        context_message = "Contexto del usuario: " + ", ".join(context_info)
        enhanced_message = f"{context_message}\n\nMensaje: {message}"
    else:
        enhanced_message = message
    
    return get_ai_response(enhanced_message, history)
