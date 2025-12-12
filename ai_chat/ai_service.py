import json
from django.conf import settings

# Import requests library explicitly
try:
    import requests as http_requests
except ImportError:
    http_requests = None


class AIService:
    """
    Servicio para interactuar con OpenRouter API
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
        self.api_url = 'https://openrouter.ai/api/v1/chat/completions'
        self.model = 'meta-llama/llama-3.1-8b-instruct:free'  # Modelo gratuito
    
    def chat(self, message, context=None, history=None):
        """
        Envía un mensaje a la IA y obtiene respuesta
        
        Args:
            message: Mensaje del usuario
            context: Contexto del sistema (métricas, datos)
            history: Historial de mensajes previos
        
        Returns:
            dict con 'content', 'tokens_used', 'model'
        """
        if not self.api_key:
            return {
                'content': 'Lo siento, el servicio de IA no está configurado. Por favor contacta al administrador.',
                'tokens_used': 0,
                'model': 'none'
            }
        
        # Construir mensajes
        messages = []
        
        # Mensaje de sistema con contexto
        system_message = self._build_system_message(context)
        messages.append({
            'role': 'system',
            'content': system_message
        })
        
        # Agregar historial si existe
        if history:
            messages.extend(history[-10:])  # Últimos 10 mensajes
        
        # Agregar mensaje actual
        messages.append({
            'role': 'user',
            'content': message
        })
        
        # Llamar a la API
        try:
            if not http_requests:
                raise Exception("Librería requests no disponible")
            
            response = http_requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': self.model,
                    'messages': messages,
                    'temperature': 0.7,
                    'max_tokens': 500,
                },
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            return {
                'content': data['choices'][0]['message']['content'],
                'tokens_used': data.get('usage', {}).get('total_tokens', 0),
                'model': self.model
            }
            
        except Exception as e:
            # Fallback a respuesta predeterminada
            print(f"Error en API de OpenRouter: {e}")
            return self._fallback_response(message, context)
    
    def _build_system_message(self, context):
        """
        Construye el mensaje de sistema con contexto
        """
        try:
            base_message = """Eres AgroAssist 🌱, el asistente virtual inteligente de la cooperativa agrícola.

TU PERSONALIDAD:
- Amigable, cercano y profesional
- Experto en agricultura y gestión cooperativa
- Proactivo en dar recomendaciones
- Claro y detallado en tus explicaciones
- Usas emojis para ser más expresivo

TU MISIÓN:
Ayudar a los usuarios a gestionar mejor su cooperativa proporcionando:
- Información precisa y actualizada
- Análisis de datos en tiempo real
- Recomendaciones prácticas
- Alertas sobre situaciones importantes
- Consejos para mejorar operaciones

FORMATO DE RESPUESTAS:
- Usa los datos actuales para dar respuestas específicas
- Incluye números, porcentajes y comparaciones
- Destaca información importante con emojis
- Sugiere acciones concretas cuando sea relevante
- Sé conversacional pero informativo
- Respuestas de 2-4 párrafos (no muy largas)

"""
            
            if context:
                base_message += "\n📊 DATOS EN TIEMPO REAL DE LA COOPERATIVA:\n\n"
                
                if 'partners' in context:
                    total = context['partners']['total']
                    nuevos = context['partners']['new_this_month']
                    base_message += f"👥 SOCIOS:\n"
                    base_message += f"   • Total activos: {total}\n"
                    base_message += f"   • Nuevos este mes: {nuevos}\n"
                    if nuevos > 0:
                        base_message += f"   • Crecimiento: +{(nuevos/total*100):.1f}% este mes\n"
                    base_message += "\n"
                
                if 'parcels' in context:
                    total_p = context['parcels']['total']
                    superficie = context['parcels']['total_surface']
                    base_message += f"🌾 PARCELAS:\n"
                    base_message += f"   • Parcelas activas: {total_p}\n"
                    base_message += f"   • Superficie total: {superficie:.2f} hectáreas\n"
                    if total_p > 0:
                        promedio = superficie / total_p
                        base_message += f"   • Promedio por parcela: {promedio:.2f} ha\n"
                    base_message += "\n"
                
                if 'sales' in context:
                    hoy_count = context['sales']['today_count']
                    hoy_amount = context['sales']['today_amount']
                    mes_count = context['sales']['this_month_count']
                    mes_amount = context['sales']['this_month_amount']
                    
                    base_message += f"💰 VENTAS:\n"
                    base_message += f"   HOY:\n"
                    base_message += f"   • Órdenes: {hoy_count}\n"
                    base_message += f"   • Monto: Bs. {hoy_amount:,.2f}\n"
                    if hoy_count > 0:
                        base_message += f"   • Promedio: Bs. {hoy_amount/hoy_count:,.2f} por venta\n"
                    
                    base_message += f"   ESTE MES:\n"
                    base_message += f"   • Órdenes: {mes_count}\n"
                    base_message += f"   • Monto: Bs. {mes_amount:,.2f}\n"
                    if mes_count > 0:
                        base_message += f"   • Promedio: Bs. {mes_amount/mes_count:,.2f} por venta\n"
                    base_message += "\n"
                
                if 'inventory' in context:
                    total_items = context['inventory']['total_items']
                    bajo_stock = context['inventory']['low_stock_items']
                    base_message += f"📦 INVENTARIO:\n"
                    base_message += f"   • Total de items: {total_items}\n"
                    base_message += f"   • Items con stock bajo: {bajo_stock}\n"
                    if bajo_stock > 0:
                        porcentaje = (bajo_stock/total_items*100) if total_items > 0 else 0
                        base_message += f"   ⚠️ {porcentaje:.1f}% del inventario necesita reabastecimiento\n"
                    base_message += "\n"
                
                if 'production' in context and context['production']['harvested_count'] > 0:
                    cosechas = context['production']['harvested_count']
                    cantidad = context['production']['total_quantity']
                    base_message += f"🚜 PRODUCCIÓN:\n"
                    base_message += f"   • Cosechas registradas: {cosechas}\n"
                    base_message += f"   • Cantidad total: {cantidad:,.2f} kg\n"
                    if cosechas > 0:
                        base_message += f"   • Promedio por cosecha: {cantidad/cosechas:,.2f} kg\n"
                    base_message += "\n"
                
                if 'goals' in context and context['goals']['active'] > 0:
                    activas = context['goals']['active']
                    completadas = context['goals']['completed']
                    progreso = context['goals']['avg_progress']
                    base_message += f"🎯 METAS:\n"
                    base_message += f"   • Metas activas: {activas}\n"
                    base_message += f"   • Metas completadas: {completadas}\n"
                    base_message += f"   • Progreso promedio: {progreso:.1f}%\n"
                    if progreso >= 75:
                        base_message += f"   ✨ ¡Excelente progreso!\n"
                    elif progreso >= 50:
                        base_message += f"   💪 Buen avance, sigue así\n"
                    else:
                        base_message += f"   📈 Necesitas acelerar el ritmo\n"
                    base_message += "\n"
                
                if 'campaigns' in context and context['campaigns']['active'] > 0:
                    base_message += f"🌱 CAMPAÑAS:\n"
                    base_message += f"   • Campañas activas: {context['campaigns']['active']}\n\n"
                
                if 'events' in context and context['events']['upcoming'] > 0:
                    base_message += f"📅 EVENTOS:\n"
                    base_message += f"   • Eventos próximos: {context['events']['upcoming']}\n\n"
            
            base_message += """
INSTRUCCIONES IMPORTANTES:
1. SIEMPRE usa los datos de arriba para responder con precisión
2. Calcula porcentajes, promedios y comparaciones cuando sea útil
3. Destaca información crítica (stock bajo, metas atrasadas, etc.)
4. Sugiere acciones específicas basadas en los datos
5. Si no tienes un dato, dilo honestamente y sugiere dónde encontrarlo
6. Sé conversacional: usa "tienes", "tu cooperativa", etc.
7. Termina con una pregunta o sugerencia cuando sea apropiado

Responde en español de forma natural, amigable y profesional.
"""
            
            return base_message
            
        except Exception as e:
            print(f"Error en _build_system_message: {e}")
            return "Eres AgroAssist, un asistente amigable para cooperativas agrícolas. Responde en español de forma clara y útil."
    
    def _fallback_response(self, message, context):
        """
        Respuesta de fallback cuando la API falla
        """
        from .fallback_responses import (
            get_partners_response,
            get_parcels_response,
            get_sales_response,
            get_inventory_response,
            get_production_response,
            get_goals_response,
            get_help_response
        )
        
        message_lower = message.lower()
        
        # Respuestas predefinidas basadas en palabras clave
        if ('socios' in message_lower or 'miembros' in message_lower or 'cuántos socios' in message_lower or
            'cooperativistas' in message_lower or 'asociados' in message_lower):
            response = get_partners_response(context)
            if response:
                return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        elif ('ventas' in message_lower or 'vendí' in message_lower or 'ingresos' in message_lower or
              'ganancias' in message_lower or 'facturación' in message_lower or 'cuánto vendí' in message_lower):
            response = get_sales_response(context)
            if response:
                return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        elif ('parcelas' in message_lower or 'terrenos' in message_lower or 'hectáreas' in message_lower or
              'superficie' in message_lower or 'tierras' in message_lower or 'lotes' in message_lower):
            response = get_parcels_response(context)
            if response:
                return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        elif ('stock' in message_lower or 'inventario' in message_lower or 'productos' in message_lower or 
              'insumos' in message_lower or 'comprar' in message_lower or 'necesito' in message_lower or
              'reabastec' in message_lower or 'falta' in message_lower):
            response = get_inventory_response(context)
            if response:
                return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        elif ('producción' in message_lower or 'cosecha' in message_lower or 'producido' in message_lower or
              'cultivado' in message_lower or 'rendimiento' in message_lower):
            response = get_production_response(context)
            if response:
                return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        elif ('metas' in message_lower or 'objetivos' in message_lower or 'progreso' in message_lower or
              'avance' in message_lower or 'cómo van' in message_lower):
            response = get_goals_response(context)
            if response:
                return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        elif ('campañas' in message_lower or 'campaña' in message_lower):
            if context and 'campaigns' in context:
                activas = context['campaigns']['active']
                response = f"🌱 **Campañas Agrícolas Activas**\n\n"
                
                if activas > 0:
                    response += f"Actualmente tienes **{activas} campañas activas** en curso.\n\n"
                    response += f"**¿Qué son las campañas?**\n"
                    response += f"Las campañas agrícolas son ciclos de producción que incluyen:\n"
                    response += f"• Preparación del terreno\n"
                    response += f"• Siembra\n"
                    response += f"• Mantenimiento y cuidado\n"
                    response += f"• Cosecha\n\n"
                    
                    response += f"**Gestión de Campañas:**\n"
                    response += f"• Revisa el estado de cada campaña en la sección Campañas\n"
                    response += f"• Registra actividades y avances\n"
                    response += f"• Monitorea costos y rendimientos\n"
                    response += f"• Planifica próximas campañas\n\n"
                    
                    response += f"¿Necesitas ayuda con alguna campaña específica?"
                else:
                    response += f"No tienes campañas activas en este momento.\n\n"
                    response += f"**Para iniciar una campaña:**\n"
                    response += f"1. Ve a la sección Campañas\n"
                    response += f"2. Crea una nueva campaña\n"
                    response += f"3. Define: cultivo, parcelas, fechas\n"
                    response += f"4. Registra actividades y costos\n"
                    response += f"5. Monitorea el progreso\n\n"
                    
                    response += f"Las campañas te ayudan a organizar mejor tu producción agrícola."
                
                return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        elif 'ayuda' in message_lower or 'qué puedes hacer' in message_lower or 'cómo funciona' in message_lower:
            response = get_help_response()
            return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        # Resumen general
        elif ('resumen' in message_lower or 'general' in message_lower or 'todo' in message_lower or
              'cómo está' in message_lower or 'estado' in message_lower):
            response = "📊 **Resumen General de tu Cooperativa**\n\n"
            
            if context:
                if 'partners' in context:
                    response += f"👥 **Socios:** {context['partners']['total']} activos ({context['partners']['new_this_month']} nuevos este mes)\n\n"
                
                if 'sales' in context:
                    response += f"💰 **Ventas hoy:** {context['sales']['today_count']} órdenes (Bs. {context['sales']['today_amount']:,.2f})\n"
                    response += f"💰 **Ventas mes:** {context['sales']['this_month_count']} órdenes (Bs. {context['sales']['this_month_amount']:,.2f})\n\n"
                
                if 'parcels' in context:
                    response += f"🌾 **Parcelas:** {context['parcels']['total']} activas ({context['parcels']['total_surface']:.1f} ha)\n\n"
                
                if 'inventory' in context and context['inventory']['low_stock_items'] > 0:
                    response += f"⚠️ **Inventario:** {context['inventory']['low_stock_items']} items necesitan reabastecimiento\n\n"
                
                if 'goals' in context and context['goals']['active'] > 0:
                    response += f"🎯 **Metas:** {context['goals']['active']} activas ({context['goals']['avg_progress']:.0f}% progreso)\n\n"
                
                response += "¿Quieres información más detallada sobre algún área específica?"
            
            return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        # Recomendaciones y consejos
        elif ('consejo' in message_lower or 'recomendación' in message_lower or 'sugerencia' in message_lower or
              'qué debo hacer' in message_lower or 'cómo mejorar' in message_lower):
            response = "💡 **Recomendaciones para tu Cooperativa**\n\n"
            
            if context:
                prioridades = []
                
                if 'inventory' in context and context['inventory']['low_stock_items'] > 0:
                    prioridades.append(f"🔴 **URGENTE:** Reabastecer {context['inventory']['low_stock_items']} productos con stock bajo")
                
                if 'goals' in context and context['goals']['avg_progress'] < 50:
                    prioridades.append(f"🟡 **IMPORTANTE:** Acelerar progreso de metas (actualmente {context['goals']['avg_progress']:.0f}%)")
                
                if 'partners' in context and context['partners']['new_this_month'] == 0:
                    prioridades.append("🟢 **SUGERENCIA:** Implementar estrategias para captar nuevos socios")
                
                if prioridades:
                    response += "**Prioridades identificadas:**\n"
                    for i, p in enumerate(prioridades, 1):
                        response += f"{i}. {p}\n"
                    response += "\n"
                
                response += "**Acciones generales recomendadas:**\n"
                response += "• Revisa tus métricas diariamente\n"
                response += "• Mantén actualizado el inventario\n"
                response += "• Registra todas las actividades\n"
                response += "• Comunícate regularmente con los socios\n"
                response += "• Analiza tendencias de ventas\n\n"
                response += "¿Necesitas ayuda específica con alguna área?"
            
            return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
        
        # Respuesta genérica con sugerencias
        response = """Lo siento, no entendí tu pregunta. 🤔

**Puedes preguntarme sobre:**
• Socios y miembros
• Ventas e ingresos  
• Parcelas y terrenos
• Inventario y stock (insumos, productos)
• Producción y cosechas
• Metas y objetivos
• Resumen general
• Recomendaciones

O escribe "ayuda" para ver todas mis capacidades."""
        
        return {'content': response, 'tokens_used': 0, 'model': 'fallback'}
