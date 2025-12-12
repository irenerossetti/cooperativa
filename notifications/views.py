from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Notification, NotificationPreference
from .serializers import (
    NotificationSerializer,
    NotificationPreferenceSerializer,
    NotificationCreateSerializer
)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar notificaciones
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """Filtra notificaciones del usuario actual"""
        user = self.request.user
        queryset = Notification.objects.filter(user=user)
        
        # Filtro por leídas/no leídas
        unread = self.request.query_params.get('unread', None)
        if unread is not None:
            if unread.lower() == 'true':
                queryset = queryset.filter(read=False)
            elif unread.lower() == 'false':
                queryset = queryset.filter(read=True)
        
        # Filtro por tipo
        notification_type = self.request.query_params.get('type', None)
        if notification_type:
            queryset = queryset.filter(type=notification_type)
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def perform_create(self, serializer):
        """Agrega el usuario actual al crear una notificación"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Obtiene el conteo de notificaciones no leídas"""
        count = Notification.objects.filter(
            user=request.user,
            read=False
        ).count()
        
        return Response({'unread_count': count})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Marca una notificación como leída"""
        notification = self.get_object()
        
        if notification.user != request.user:
            return Response(
                {'error': 'No tienes permiso para marcar esta notificación'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notification.mark_as_read()
        
        return Response({
            'message': 'Notificación marcada como leída',
            'notification': NotificationSerializer(notification).data
        })

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Marca todas las notificaciones como leídas"""
        from django.utils import timezone
        
        updated = Notification.objects.filter(
            user=request.user,
            read=False
        ).update(
            read=True,
            read_at=timezone.now()
        )
        
        return Response({
            'message': f'{updated} notificaciones marcadas como leídas',
            'count': updated
        })

    @action(detail=False, methods=['delete'])
    def delete_all_read(self, request):
        """Elimina todas las notificaciones leídas"""
        deleted, _ = Notification.objects.filter(
            user=request.user,
            read=True
        ).delete()
        
        return Response({
            'message': f'{deleted} notificaciones eliminadas',
            'count': deleted
        })

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Obtiene las últimas 10 notificaciones"""
        notifications = Notification.objects.filter(
            user=request.user
        )[:10]
        
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar preferencias de notificación
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationPreferenceSerializer
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        """Solo las preferencias del usuario actual"""
        return NotificationPreference.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_preferences(self, request):
        """Obtiene o crea las preferencias del usuario actual"""
        preferences, created = NotificationPreference.objects.get_or_create(
            user=request.user
        )
        
        serializer = self.get_serializer(preferences)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_preferences(self, request):
        """Actualiza las preferencias del usuario actual"""
        preferences, created = NotificationPreference.objects.get_or_create(
            user=request.user
        )
        
        serializer = self.get_serializer(
            preferences,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Preferencias actualizadas correctamente',
            'preferences': serializer.data
        })
