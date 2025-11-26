from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ChatConversation, ChatMessage
from .chatbot_engine import process_message
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot_api(request):
    """
    Endpoint principal del chatbot
    Recibe un mensaje y devuelve una respuesta inteligente
    """
    try:
        message = request.data.get('message', '').strip()
        cliente_id = request.data.get('cliente_id')

        if not message:
            return Response(
                {'error': 'El mensaje no puede estar vacío'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not cliente_id:
            # Generar un cliente_id único si no se proporciona
            import uuid
            cliente_id = f"user_{uuid.uuid4().hex[:12]}"

        # Obtener organización del usuario
        organization = None
        if hasattr(request.user, 'organization'):
            organization = request.user.organization
        elif hasattr(request.user, 'partner') and hasattr(request.user.partner, 'organization'):
            organization = request.user.partner.organization
        
        # Si no hay organización, usar la primera disponible o crear una por defecto
        if not organization:
            from tenants.models import Organization
            organization = Organization.objects.first()
            if not organization:
                # Crear organización por defecto si no existe
                organization = Organization.objects.create(
                    name='Cooperativa Demo',
                    slug='cooperativa-demo',
                    subdomain='demo'
                )

        # Obtener o crear conversación
        conversation, created = ChatConversation.objects.get_or_create(
            cliente_id=cliente_id,
            organization=organization,
            defaults={'fase': 'exploracion'}
        )

        # Guardar mensaje del usuario
        ChatMessage.objects.create(
            conversation=conversation,
            message_type='user',
            content=message
        )

        # Procesar mensaje y obtener respuesta
        response_text = process_message(message, conversation)

        # Guardar respuesta del bot
        ChatMessage.objects.create(
            conversation=conversation,
            message_type='bot',
            content=response_text
        )

        return Response({
            'response': response_text,
            'cliente_id': cliente_id,
            'conversation_id': conversation.id
        })

    except Exception as e:
        logger.error(f"Error en chatbot_api: {str(e)}")
        return Response(
            {'error': 'Error al procesar el mensaje', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_historial(request, cliente_id):
    """
    Obtiene el historial de conversación de un cliente
    """
    try:
        # Obtener organización del usuario
        organization = None
        if hasattr(request.user, 'organization'):
            organization = request.user.organization
        elif hasattr(request.user, 'partner') and hasattr(request.user.partner, 'organization'):
            organization = request.user.partner.organization
        
        if not organization:
            from tenants.models import Organization
            organization = Organization.objects.first()
        
        conversation = ChatConversation.objects.filter(
            cliente_id=cliente_id,
            organization=organization
        ).first()
        
        if not conversation:
            return Response({
                'cliente_id': cliente_id,
                'historial': {
                    'interaccion': [],
                    'respuestas_bot': [],
                    'fase': 'exploracion'
                }
            })

        messages = conversation.messages.all()
        user_messages = [msg.content for msg in messages if msg.message_type == 'user']
        bot_messages = [msg.content for msg in messages if msg.message_type == 'bot']

        return Response({
            'cliente_id': cliente_id,
            'historial': {
                'nombre': conversation.nombre,
                'edad': conversation.edad,
                'tipo_cultivo': conversation.tipo_cultivo,
                'necesidad_principal': conversation.necesidad_principal,
                'fase': conversation.fase,
                'tono': conversation.tono,
                'nivel_interes': conversation.nivel_interes,
                'interaccion': user_messages,
                'respuestas_bot': bot_messages,
                'total_mensajes': messages.count()
            }
        })

    except Exception as e:
        logger.error(f"Error al obtener historial: {str(e)}")
        return Response(
            {'error': 'Error al obtener historial'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def limpiar_historial(request, cliente_id):
    """
    Limpia el historial de conversación de un cliente
    """
    try:
        # Obtener organización del usuario
        organization = None
        if hasattr(request.user, 'organization'):
            organization = request.user.organization
        elif hasattr(request.user, 'partner') and hasattr(request.user.partner, 'organization'):
            organization = request.user.partner.organization
        
        if not organization:
            from tenants.models import Organization
            organization = Organization.objects.first()
        
        deleted_count, _ = ChatConversation.objects.filter(
            cliente_id=cliente_id,
            organization=organization
        ).delete()
        
        return Response({
            'mensaje': f'Historial limpiado para cliente {cliente_id}',
            'cliente_id': cliente_id,
            'conversaciones_eliminadas': deleted_count
        })

    except Exception as e:
        logger.error(f"Error al limpiar historial: {str(e)}")
        return Response(
            {'error': 'Error al limpiar historial'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
