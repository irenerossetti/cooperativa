from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum
from .models import ChatConversation, ChatMessage
from .serializers import (
    ChatConversationSerializer,
    ChatMessageSerializer,
    ChatRequestSerializer
)
from .ai_service import AIService


class ChatConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar conversaciones de chat
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChatConversationSerializer

    def get_queryset(self):
        return ChatConversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def chat(self, request):
        """
        Endpoint principal para chatear con la IA
        """
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message = serializer.validated_data['message']
        conversation_id = serializer.validated_data.get('conversation_id')
        include_context = serializer.validated_data.get('include_context', True)
        
        # Obtener o crear conversación
        if conversation_id:
            try:
                conversation = ChatConversation.objects.get(
                    id=conversation_id,
                    user=request.user
                )
            except ChatConversation.DoesNotExist:
                return Response(
                    {'error': 'Conversación no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Crear nueva conversación
            conversation = ChatConversation.objects.create(
                user=request.user,
                title=message[:50] + ('...' if len(message) > 50 else '')
            )
        
        # Guardar mensaje del usuario
        user_message = ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=message
        )
        
        # Obtener contexto del sistema si se solicita
        context = None
        if include_context:
            context = self._get_system_context(request.user)
        
        # Obtener historial de la conversación
        history = list(conversation.messages.values('role', 'content'))
        
        # Llamar al servicio de IA
        ai_service = AIService()
        try:
            ai_response = ai_service.chat(
                message=message,
                context=context,
                history=history[:-1]  # Excluir el último mensaje (el actual)
            )
            
            # Guardar respuesta de la IA
            assistant_message = ChatMessage.objects.create(
                conversation=conversation,
                role='assistant',
                content=ai_response['content'],
                tokens_used=ai_response.get('tokens_used'),
                model_used=ai_response.get('model')
            )
            
            return Response({
                'conversation_id': conversation.id,
                'user_message': ChatMessageSerializer(user_message).data,
                'assistant_message': ChatMessageSerializer(assistant_message).data,
                'context_used': include_context
            })
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"Error en chat: {error_detail}")
            
            # Crear mensaje de error para el usuario
            assistant_message = ChatMessage.objects.create(
                conversation=conversation,
                role='assistant',
                content=f'Lo siento, ocurrió un error al procesar tu mensaje. Por favor intenta de nuevo.',
                tokens_used=0,
                model_used='error'
            )
            
            return Response({
                'conversation_id': conversation.id,
                'user_message': ChatMessageSerializer(user_message).data,
                'assistant_message': ChatMessageSerializer(assistant_message).data,
                'context_used': include_context,
                'error': str(e)
            })

    @action(detail=True, methods=['delete'])
    def clear(self, request, pk=None):
        """Elimina todos los mensajes de una conversación"""
        conversation = self.get_object()
        deleted_count = conversation.messages.all().delete()[0]
        
        return Response({
            'message': f'{deleted_count} mensajes eliminados',
            'conversation_id': conversation.id
        })

    def _get_system_context(self, user):
        """
        Obtiene contexto del sistema para la IA
        """
        try:
            from partners.models import Partner
            from parcels.models import Parcel
            from sales.models import Order
            from inventory.models import InventoryItem, StockAlert
            from campaigns.models import Campaign
            from django.utils import timezone
            from datetime import timedelta
            
            today = timezone.now().date()
            this_month_start = today.replace(day=1)
            
            # Recopilar métricas de forma segura
            context = {
                'user': {
                    'name': user.get_full_name() or user.username,
                    'role': user.role.name if hasattr(user, 'role') and user.role else 'Usuario'
                }
            }
            
            # Partners
            try:
                context['partners'] = {
                    'total': Partner.objects.filter(status='ACTIVE').count(),
                    'new_this_month': Partner.objects.filter(
                        registration_date__gte=this_month_start
                    ).count()
                }
            except Exception as e:
                print(f"Error obteniendo partners: {e}")
                context['partners'] = {'total': 0, 'new_this_month': 0}
            
            # Parcels
            try:
                from django.db.models import Sum as DbSum
                parcels_qs = Parcel.objects.filter(status='ACTIVE')
                total_surface = parcels_qs.aggregate(total=DbSum('surface'))['total']
                context['parcels'] = {
                    'total': parcels_qs.count(),
                    'total_surface': float(total_surface) if total_surface else 0.0
                }
            except Exception as e:
                print(f"Error obteniendo parcels: {e}")
                context['parcels'] = {'total': 0, 'total_surface': 0.0}
            
            # Sales
            try:
                from django.db.models import Sum as DbSum
                from datetime import datetime
                
                # Convertir today a datetime para comparar
                today_start = datetime.combine(today, datetime.min.time())
                today_end = datetime.combine(today, datetime.max.time())
                
                today_orders = Order.objects.filter(
                    order_date__gte=today_start,
                    order_date__lte=today_end
                )
                month_orders = Order.objects.filter(order_date__gte=this_month_start)
                
                today_total = today_orders.aggregate(total=DbSum('total_amount'))['total']
                month_total = month_orders.aggregate(total=DbSum('total_amount'))['total']
                
                context['sales'] = {
                    'today_count': today_orders.count(),
                    'today_amount': float(today_total) if today_total else 0.0,
                    'this_month_count': month_orders.count(),
                    'this_month_amount': float(month_total) if month_total else 0.0
                }
            except Exception as e:
                print(f"Error obteniendo sales: {e}")
                context['sales'] = {
                    'today_count': 0, 'today_amount': 0.0,
                    'this_month_count': 0, 'this_month_amount': 0.0
                }
            
            # Inventory
            try:
                low_stock_alerts = StockAlert.objects.filter(is_resolved=False).select_related('item')
                low_stock_products = []
                
                for alert in low_stock_alerts[:10]:  # Máximo 10 productos
                    low_stock_products.append({
                        'name': alert.item.name if hasattr(alert.item, 'name') else f'Item #{alert.item.id}',
                        'current_stock': alert.current_stock,
                        'minimum_stock': alert.minimum_stock
                    })
                
                context['inventory'] = {
                    'low_stock_items': low_stock_alerts.count(),
                    'total_items': InventoryItem.objects.count(),
                    'low_stock_products': low_stock_products
                }
            except Exception as e:
                print(f"Error obteniendo inventory: {e}")
                context['inventory'] = {'low_stock_items': 0, 'total_items': 0, 'low_stock_products': []}
            
            # Campaigns
            try:
                context['campaigns'] = {
                    'active': Campaign.objects.filter(status='ACTIVE').count()
                }
            except Exception as e:
                print(f"Error obteniendo campaigns: {e}")
                context['campaigns'] = {'active': 0}
            
            # Production
            try:
                from production.models import HarvestedProduct
                from django.db.models import Sum as DbSum
                harvested = HarvestedProduct.objects.all()
                total_qty = harvested.aggregate(total=DbSum('quantity'))['total']
                context['production'] = {
                    'harvested_count': harvested.count(),
                    'total_quantity': float(total_qty) if total_qty else 0.0
                }
            except Exception as e:
                print(f"Error obteniendo production: {e}")
                context['production'] = {'harvested_count': 0, 'total_quantity': 0.0}
            
            # Goals
            try:
                from goals.models import Goal
                goals = Goal.objects.all()
                active_goals = goals.exclude(status='COMPLETED').exclude(status='CANCELLED')
                completed_goals = goals.filter(status='COMPLETED')
                
                # Calcular progreso promedio
                avg_progress = 0
                if active_goals.exists():
                    total_progress = sum([
                        (g.current_value / g.target_value * 100) if g.target_value > 0 else 0
                        for g in active_goals
                    ])
                    avg_progress = total_progress / active_goals.count()
                
                context['goals'] = {
                    'active': active_goals.count(),
                    'completed': completed_goals.count(),
                    'avg_progress': avg_progress
                }
            except Exception as e:
                print(f"Error obteniendo goals: {e}")
                context['goals'] = {'active': 0, 'completed': 0, 'avg_progress': 0}
            
            # Events
            try:
                from events.models import Event
                upcoming_events = Event.objects.filter(
                    start_datetime__gte=timezone.now()
                ).count()
                context['events'] = {
                    'upcoming': upcoming_events
                }
            except Exception as e:
                print(f"Error obteniendo events: {e}")
                context['events'] = {'upcoming': 0}
            
            return context
            
        except Exception as e:
            print(f"Error general en _get_system_context: {e}")
            return {
                'user': {
                    'name': user.get_full_name() or user.username,
                    'role': 'Usuario'
                }
            }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quick_question(request):
    """
    Endpoint para preguntas rápidas sin guardar historial
    """
    # Aceptar tanto 'question' como 'message'
    question = request.data.get('question') or request.data.get('message')
    
    if not question:
        return Response(
            {'error': 'La pregunta o mensaje es requerido'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtener contexto
    viewset = ChatConversationViewSet()
    context = viewset._get_system_context(request.user)
    
    # Llamar al servicio de IA
    ai_service = AIService()
    try:
        ai_response = ai_service.chat(
            message=question,
            context=context,
            history=[]
        )
        
        return Response({
            'question': question,
            'answer': ai_response['content'],
            'tokens_used': ai_response.get('tokens_used'),
            'model': ai_response.get('model')
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error al procesar la pregunta: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
