from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import AuditLog
from .serializers import AuditLogSerializer
from users.permissions import IsAdmin


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consulta de registros de auditoría (solo lectura)"""
    queryset = AuditLog.objects.select_related('user')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        user = self.request.query_params.get('user', None)
        action = self.request.query_params.get('action', None)
        model_name = self.request.query_params.get('model_name', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        search = self.request.query_params.get('search', None)
        
        if user:
            queryset = queryset.filter(user_id=user)
        
        if action:
            queryset = queryset.filter(action=action)
        
        if model_name:
            queryset = queryset.filter(model_name=model_name)
        
        if date_from:
            queryset = queryset.filter(timestamp__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(timestamp__lte=date_to)
        
        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) |
                Q(user__username__icontains=search)
            )
        
        return queryset
