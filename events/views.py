from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import Event, EventReminder
from .serializers import EventSerializer, EventReminderSerializer, EventCalendarSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar eventos del calendario
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Filtro por tipo
        event_type = self.request.query_params.get('type', None)
        if event_type:
            queryset = queryset.filter(type=event_type)
        
        # Filtro por rango de fechas
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(start_datetime__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_datetime__lte=end_date)
        
        # Filtro por completado
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            queryset = queryset.filter(completed=completed.lower() == 'true')
        
        # Filtro por parcela
        parcel_id = self.request.query_params.get('parcel', None)
        if parcel_id:
            queryset = queryset.filter(parcels__id=parcel_id)
        
        # Filtro por participante
        participant_id = self.request.query_params.get('participant', None)
        if participant_id:
            queryset = queryset.filter(participants__id=participant_id)
        
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == 'calendar':
            return EventCalendarSerializer
        return EventSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def calendar(self, request):
        """
        Obtiene eventos para vista de calendario
        Formato optimizado para FullCalendar
        """
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        
        queryset = self.get_queryset()
        
        if start_date:
            queryset = queryset.filter(start_datetime__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_datetime__lte=end_date)
        
        serializer = EventCalendarSerializer(queryset, many=True)
        
        # Formatear para FullCalendar
        events = []
        for event in serializer.data:
            events.append({
                'id': event['id'],
                'title': event['title'],
                'start': event['start_datetime'],
                'end': event['end_datetime'],
                'allDay': event['all_day'],
                'backgroundColor': event['color'],
                'borderColor': event['color'],
                'extendedProps': {
                    'type': event['type'],
                    'priority': event['priority'],
                    'completed': event['completed']
                }
            })
        
        return Response(events)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Obtiene eventos próximos (próximos 7 días)"""
        now = timezone.now()
        next_week = now + timedelta(days=7)
        
        events = Event.objects.filter(
            start_datetime__gte=now,
            start_datetime__lte=next_week,
            completed=False
        ).order_by('start_datetime')
        
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Obtiene eventos de hoy"""
        today = timezone.now().date()
        
        events = Event.objects.filter(
            start_datetime__date=today
        ).order_by('start_datetime')
        
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Marca un evento como completado"""
        event = self.get_object()
        event.completed = True
        event.save()
        
        serializer = self.get_serializer(event)
        return Response({
            'message': 'Evento marcado como completado',
            'event': serializer.data
        })

    @action(detail=True, methods=['post'])
    def send_reminder(self, request, pk=None):
        """Envía recordatorio del evento a los participantes"""
        event = self.get_object()
        
        if event.reminder_sent:
            return Response(
                {'message': 'El recordatorio ya fue enviado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Enviar recordatorios
        reminders_sent = []
        for participant in event.participants.all():
            # Crear notificación
            from notifications.utils import create_notification
            
            create_notification(
                user=participant,
                title=f'Recordatorio: {event.title}',
                message=f'Evento programado para {event.start_datetime.strftime("%d/%m/%Y %H:%M")}. Ubicación: {event.location or "No especificada"}',
                notification_type='INFO',
                extra_data={
                    'event_id': event.id,
                    'event_type': event.type
                }
            )
            
            # Registrar recordatorio
            reminder = EventReminder.objects.create(
                event=event,
                user=participant,
                method='NOTIFICATION'
            )
            reminders_sent.append(reminder)
        
        # Marcar como enviado
        event.reminder_sent = True
        event.save()
        
        return Response({
            'message': f'Recordatorios enviados a {len(reminders_sent)} participantes',
            'count': len(reminders_sent)
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtiene estadísticas de eventos"""
        now = timezone.now()
        
        stats = {
            'total': Event.objects.count(),
            'upcoming': Event.objects.filter(
                start_datetime__gte=now,
                completed=False
            ).count(),
            'completed': Event.objects.filter(completed=True).count(),
            'today': Event.objects.filter(
                start_datetime__date=now.date()
            ).count(),
            'by_type': {},
            'by_priority': {}
        }
        
        # Por tipo
        for choice in Event.TYPE_CHOICES:
            count = Event.objects.filter(type=choice[0]).count()
            if count > 0:
                stats['by_type'][choice[0]] = {
                    'label': choice[1],
                    'count': count
                }
        
        # Por prioridad
        for choice in Event.PRIORITY_CHOICES:
            count = Event.objects.filter(priority=choice[0]).count()
            if count > 0:
                stats['by_priority'][choice[0]] = {
                    'label': choice[1],
                    'count': count
                }
        
        return Response(stats)


class EventReminderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver recordatorios de eventos
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EventReminderSerializer
    queryset = EventReminder.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrar por usuario
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filtrar por evento
        event_id = self.request.query_params.get('event', None)
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        
        return queryset
