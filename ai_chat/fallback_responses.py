"""
Respuestas fallback detalladas para el asistente IA
"""

def get_partners_response(context):
    """Respuesta sobre socios"""
    if not context or 'partners' not in context:
        return None
    
    total = context['partners']['total']
    nuevos = context['partners']['new_this_month']
    
    response = f"👥 **Información Completa de Socios**\n\n"
    response += f"Actualmente tu cooperativa cuenta con **{total} socios activos**. "
    
    if nuevos > 0:
        crecimiento = (nuevos / total * 100) if total > 0 else 0
        response += f"Este mes se han registrado **{nuevos} nuevos socios**, "
        response += f"lo que representa un crecimiento del **{crecimiento:.1f}%**. ¡Excelente! 📈\n\n"
        response += "**Análisis:**\n"
        response += f"• La cooperativa está en fase de crecimiento\n"
        response += f"• Ritmo de incorporación: {nuevos} socios/mes\n"
        response += f"• Proyección anual: ~{nuevos * 12} nuevos socios\n\n"
        response += "**Recomendaciones:**\n"
        response += "✓ Mantén este ritmo de crecimiento\n"
        response += "✓ Asegura una buena integración de nuevos miembros\n"
        response += "✓ Considera programas de capacitación para nuevos socios"
    else:
        response += f"Este mes aún no se han registrado nuevos socios.\n\n"
        response += "**Sugerencias para captar nuevos socios:**\n"
        response += "• Organiza jornadas de puertas abiertas\n"
        response += "• Ofrece beneficios atractivos para nuevos miembros\n"
        response += "• Comparte casos de éxito de socios actuales\n"
        response += "• Facilita el proceso de registro"
    
    response += "\n\n¿Te gustaría ver más detalles sobre algún socio en particular?"
    
    return response


def get_parcels_response(context):
    """Respuesta sobre parcelas"""
    if not context or 'parcels' not in context:
        return None
    
    total = context['parcels']['total']
    superficie = context['parcels']['total_surface']
    
    response = f"🌾 **Información Detallada de Parcelas**\n\n"
    response += f"Tu cooperativa gestiona **{total} parcelas activas** con una superficie total de **{superficie:.2f} hectáreas**.\n\n"
    
    if total > 0:
        promedio = superficie / total
        response += f"**Estadísticas:**\n"
        response += f"• Superficie promedio por parcela: **{promedio:.2f} hectáreas**\n"
        
        if promedio < 1:
            response += f"• Clasificación: Parcelas pequeñas (minifundio)\n"
            response += f"• Recomendación: Considera técnicas de agricultura intensiva\n"
        elif promedio < 5:
            response += f"• Clasificación: Parcelas medianas\n"
            response += f"• Recomendación: Óptimo para diversificación de cultivos\n"
        else:
            response += f"• Clasificación: Parcelas grandes\n"
            response += f"• Recomendación: Ideal para cultivos extensivos\n"
        
        response += f"\n**Potencial Productivo:**\n"
        response += f"• Con {superficie:.2f} ha, puedes producir aproximadamente:\n"
        response += f"  - Café: ~{superficie * 800:.0f} kg/año\n"
        response += f"  - Quinua: ~{superficie * 1200:.0f} kg/año\n"
        response += f"  - Maíz: ~{superficie * 2000:.0f} kg/año\n"
        
        response += f"\n**Gestión:**\n"
        response += f"• Puedes ver el detalle de cada parcela en la sección Parcelas\n"
        response += f"• Registra actividades agrícolas para mejor seguimiento\n"
        response += f"• Monitorea el rendimiento por parcela"
    
    response += "\n\n¿Quieres información sobre alguna parcela específica?"
    
    return response


def get_sales_response(context):
    """Respuesta sobre ventas"""
    if not context or 'sales' not in context:
        return None
    
    hoy_count = context['sales']['today_count']
    hoy_amount = context['sales']['today_amount']
    mes_count = context['sales']['this_month_count']
    mes_amount = context['sales']['this_month_amount']
    
    response = f"💰 **Análisis Completo de Ventas**\n\n"
    
    # Ventas de hoy
    response += f"**📅 VENTAS DE HOY:**\n"
    if hoy_count > 0:
        promedio_hoy = hoy_amount / hoy_count
        response += f"• Órdenes procesadas: **{hoy_count}**\n"
        response += f"• Ingresos totales: **Bs. {hoy_amount:,.2f}**\n"
        response += f"• Ticket promedio: **Bs. {promedio_hoy:,.2f}**\n"
        response += f"• Estado: {'🔥 ¡Día productivo!' if hoy_count >= 5 else '📊 Día normal'}\n"
    else:
        response += f"• Aún no hay ventas registradas hoy\n"
        response += f"• Sugerencia: Revisa pedidos pendientes o contacta clientes\n"
    
    # Ventas del mes
    response += f"\n**📊 VENTAS DEL MES:**\n"
    if mes_count > 0:
        promedio_mes = mes_amount / mes_count
        response += f"• Total de órdenes: **{mes_count}**\n"
        response += f"• Ingresos acumulados: **Bs. {mes_amount:,.2f}**\n"
        response += f"• Ticket promedio: **Bs. {promedio_mes:,.2f}**\n"
        response += f"• Promedio diario: **{mes_count/30:.1f} órdenes/día**\n"
        
        # Proyección
        dias_transcurridos = 15  # Aproximado
        proyeccion = (mes_amount / dias_transcurridos) * 30
        response += f"\n**📈 PROYECCIÓN MENSUAL:**\n"
        response += f"• Ingresos proyectados: **Bs. {proyeccion:,.2f}**\n"
        
        # Recomendaciones
        response += f"\n**💡 RECOMENDACIONES:**\n"
        if promedio_mes < 300:
            response += f"• Considera ofrecer paquetes o combos para aumentar ticket promedio\n"
        if mes_count < 50:
            response += f"• Implementa estrategias de marketing para aumentar volumen\n"
        response += f"• Analiza tus productos más vendidos\n"
        response += f"• Mantén un seguimiento diario de ventas"
    else:
        response += f"• No hay ventas registradas este mes\n"
        response += f"• Acción urgente: Revisa tu estrategia comercial\n"
    
    response += "\n\n¿Quieres ver un análisis más detallado de tus productos?"
    
    return response


def get_inventory_response(context):
    """Respuesta sobre inventario"""
    if not context or 'inventory' not in context:
        return None
    
    total = context['inventory']['total_items']
    bajo_stock = context['inventory']['low_stock_items']
    
    response = f"📦 **Estado Completo del Inventario**\n\n"
    response += f"Tu inventario cuenta con **{total} items diferentes** registrados.\n\n"
    
    # Obtener lista de productos con stock bajo
    productos_bajo_stock = context['inventory'].get('low_stock_products', [])
    
    if bajo_stock > 0:
        porcentaje = (bajo_stock / total * 100) if total > 0 else 0
        response += f"⚠️ **ALERTA DE STOCK:**\n"
        response += f"• Items con stock bajo: **{bajo_stock}** ({porcentaje:.1f}% del inventario)\n"
        response += f"• Prioridad: {'🔴 ALTA' if porcentaje > 20 else '🟡 MEDIA'}\n\n"
        
        # Mostrar lista de productos si está disponible
        if productos_bajo_stock:
            response += f"\n**PRODUCTOS QUE NECESITAS COMPRAR:**\n"
            for i, producto in enumerate(productos_bajo_stock[:10], 1):  # Máximo 10
                nombre = producto.get('name', 'Producto')
                stock = producto.get('current_stock', 0)
                minimo = producto.get('minimum_stock', 0)
                response += f"{i}. **{nombre}** - Stock actual: {stock} (mínimo: {minimo})\n"
            
            if len(productos_bajo_stock) > 10:
                response += f"\n... y {len(productos_bajo_stock) - 10} productos más\n"
            response += "\n"
        
        response += f"**ACCIONES RECOMENDADAS:**\n"
        response += f"1. Programa pedidos de reabastecimiento esta semana\n"
        response += f"2. Contacta a tus proveedores habituales\n"
        response += f"3. Considera compras al por mayor para mejores precios\n"
        response += f"4. Revisa la sección Inventario para más detalles\n\n"
        
        response += f"**IMPACTO:**\n"
        response += f"• Riesgo de perder ventas por falta de stock\n"
        response += f"• Posible insatisfacción de clientes\n"
        response += f"• Oportunidad de optimizar niveles de inventario\n"
    else:
        response += f"✅ **ESTADO ÓPTIMO:**\n"
        response += f"• Todos los productos tienen stock adecuado\n"
        response += f"• No hay alertas de reabastecimiento\n"
        response += f"• Gestión de inventario eficiente\n\n"
        
        response += f"**MANTÉN ESTE NIVEL:**\n"
        response += f"• Revisa inventario semanalmente\n"
        response += f"• Actualiza niveles mínimos según demanda\n"
        response += f"• Registra entradas y salidas puntualmente\n"
    
    response += f"\n**GESTIÓN INTELIGENTE:**\n"
    response += f"• Configura alertas automáticas de stock mínimo\n"
    response += f"• Analiza rotación de productos\n"
    response += f"• Identifica productos de baja rotación\n"
    
    response += "\n\n¿Necesitas ayuda con algún producto específico?"
    
    return response


def get_production_response(context):
    """Respuesta sobre producción"""
    if not context or 'production' not in context:
        return None
    
    cosechas = context['production']['harvested_count']
    cantidad = context['production']['total_quantity']
    
    response = f"🚜 **Análisis de Producción Agrícola**\n\n"
    
    if cosechas > 0:
        promedio = cantidad / cosechas
        response += f"Has registrado **{cosechas} cosechas** con un total de **{cantidad:,.2f} kg** producidos.\n\n"
        
        response += f"**ESTADÍSTICAS:**\n"
        response += f"• Producción promedio por cosecha: **{promedio:,.2f} kg**\n"
        response += f"• Rendimiento: {'🌟 Excelente' if promedio > 500 else '📊 Normal'}\n\n"
        
        response += f"**ANÁLISIS:**\n"
        if promedio > 500:
            response += f"• Tu rendimiento está por encima del promedio\n"
            response += f"• Mantén las buenas prácticas agrícolas\n"
        else:
            response += f"• Hay oportunidad de mejorar el rendimiento\n"
            response += f"• Considera: mejor fertilización, riego adecuado, control de plagas\n"
        
        response += f"\n**VALOR ESTIMADO:**\n"
        response += f"• A Bs. 15/kg: **Bs. {cantidad * 15:,.2f}**\n"
        response += f"• A Bs. 20/kg: **Bs. {cantidad * 20:,.2f}**\n"
        response += f"• A Bs. 25/kg: **Bs. {cantidad * 25:,.2f}**\n"
        
        response += f"\n**RECOMENDACIONES:**\n"
        response += f"• Registra todas las cosechas para mejor análisis\n"
        response += f"• Compara rendimiento entre parcelas\n"
        response += f"• Identifica mejores prácticas\n"
        response += f"• Planifica próximas siembras basándote en estos datos\n"
    else:
        response += f"Aún no hay cosechas registradas en el sistema.\n\n"
        response += f"**PARA EMPEZAR:**\n"
        response += f"• Registra tus cosechas en la sección Producción\n"
        response += f"• Incluye: fecha, parcela, cultivo, cantidad\n"
        response += f"• Esto te permitirá analizar rendimientos\n"
        response += f"• Podrás tomar mejores decisiones agrícolas\n"
    
    response += "\n\n¿Quieres consejos para mejorar tu producción?"
    
    return response


def get_goals_response(context):
    """Respuesta sobre metas"""
    if not context or 'goals' not in context:
        return None
    
    activas = context['goals']['active']
    completadas = context['goals']['completed']
    progreso = context['goals']['avg_progress']
    
    response = f"🎯 **Estado de Metas y Objetivos**\n\n"
    
    if activas > 0:
        response += f"Tienes **{activas} metas activas** con un progreso promedio del **{progreso:.1f}%**.\n"
        response += f"Has completado **{completadas} metas** hasta ahora.\n\n"
        
        # Evaluación del progreso
        response += f"**EVALUACIÓN:**\n"
        if progreso >= 75:
            response += f"✨ **¡Excelente progreso!**\n"
            response += f"• Estás muy cerca de alcanzar tus objetivos\n"
            response += f"• Mantén el ritmo actual\n"
            response += f"• Celebra los logros con tu equipo\n"
        elif progreso >= 50:
            response += f"💪 **Buen avance**\n"
            response += f"• Vas por buen camino\n"
            response += f"• Mantén la constancia\n"
            response += f"• Identifica obstáculos y resuélvelos\n"
        elif progreso >= 25:
            response += f"📈 **Necesitas acelerar**\n"
            response += f"• El progreso es lento\n"
            response += f"• Revisa tu estrategia\n"
            response += f"• Prioriza acciones de alto impacto\n"
        else:
            response += f"🚨 **Atención requerida**\n"
            response += f"• El progreso está muy bajo\n"
            response += f"• Urgente: replantea tus metas o estrategia\n"
            response += f"• Considera dividir metas grandes en hitos pequeños\n"
        
        response += f"\n**RECOMENDACIONES:**\n"
        response += f"• Revisa tus metas semanalmente\n"
        response += f"• Actualiza el progreso regularmente\n"
        response += f"• Celebra cada hito alcanzado\n"
        response += f"• Ajusta metas si es necesario\n"
        
        response += f"\n**PRÓXIMOS PASOS:**\n"
        response += f"• Identifica la meta más cercana a completarse\n"
        response += f"• Enfoca esfuerzos en metas prioritarias\n"
        response += f"• Documenta lecciones aprendidas\n"
    else:
        response += f"No tienes metas activas en este momento.\n\n"
        response += f"**¿POR QUÉ ESTABLECER METAS?**\n"
        response += f"• Dan dirección clara a tu cooperativa\n"
        response += f"• Motivan al equipo\n"
        response += f"• Permiten medir progreso\n"
        response += f"• Facilitan la toma de decisiones\n\n"
        
        response += f"**SUGERENCIAS DE METAS:**\n"
        response += f"• Aumentar producción en 20%\n"
        response += f"• Incrementar ventas mensuales\n"
        response += f"• Captar 10 nuevos socios\n"
        response += f"• Mejorar calidad de productos\n"
        response += f"• Reducir costos operativos\n"
    
    response += "\n\n¿Te ayudo a crear o ajustar alguna meta?"
    
    return response


def get_help_response():
    """Respuesta de ayuda"""
    response = """🤖 **¡Hola! Soy AgroAssist, tu asistente virtual** 👋

Estoy aquí para ayudarte a gestionar tu cooperativa de forma más eficiente. Tengo acceso a todos los datos en tiempo real y puedo ayudarte con:

**📊 INFORMACIÓN Y ANÁLISIS:**
• Socios y miembros de la cooperativa
• Parcelas y superficie cultivada
• Ventas e ingresos (diarios y mensuales)
• Inventario y alertas de stock
• Producción y cosechas
• Metas y su progreso
• Eventos y calendario
• Campañas agrícolas activas

**💡 RECOMENDACIONES:**
• Consejos para mejorar operaciones
• Análisis de rendimiento
• Identificación de áreas de oportunidad
• Sugerencias de acciones prioritarias

**🎯 EJEMPLOS DE PREGUNTAS:**
• "¿Cuántos socios tengo?"
• "¿Cuánto vendí este mes?"
• "¿Qué productos tienen stock bajo?"
• "¿Cómo van mis metas?"
• "Dame un resumen general"
• "¿Qué debo hacer hoy?"

**✨ MIS CAPACIDADES:**
• Respondo en tiempo real con datos actualizados
• Calculo estadísticas y promedios
• Identifico problemas y oportunidades
• Sugiero acciones concretas
• Explico de forma clara y amigable

¡Pregúntame lo que necesites! Estoy aquí para ayudarte 😊"""
    
    return response
