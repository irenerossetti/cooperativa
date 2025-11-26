import os
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
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
    
    @action(detail=False, methods=['get'], url_path='developer-access', 
            permission_classes=[])
    def developer_access(self, request):
        """
        Acceso especial con llave de desarrollador única.
        Este endpoint permite acceso completo a todos los logs sin restricciones
        de tenant, pero requiere una llave secreta de desarrollador.
        
        Header requerido: X-Developer-Key
        """
        developer_key = request.headers.get('X-Developer-Key')
        expected_key = os.getenv('AUDIT_DEVELOPER_KEY')
        
        # Validar que existe la llave configurada
        if not expected_key:
            return Response(
                {
                    'error': 'Sistema de llave de desarrollador no configurado',
                    'detail': 'Configure AUDIT_DEVELOPER_KEY en variables de entorno'
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Validar la llave proporcionada
        if not developer_key or developer_key != expected_key:
            return Response(
                {
                    'error': 'Acceso denegado',
                    'detail': 'Llave de desarrollador inválida o no proporcionada'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Acceso completo sin restricciones de tenant
        # Usar .all() directamente en el modelo para bypass del TenantManager
        from django.db import connection
        queryset = AuditLog.objects.all().select_related('user').order_by('-timestamp')
        
        # Aplicar filtros opcionales
        user = request.query_params.get('user', None)
        action = request.query_params.get('action', None)
        organization = request.query_params.get('organization', None)
        
        if user:
            queryset = queryset.filter(user_id=user)
        if action:
            queryset = queryset.filter(action=action)
        if organization:
            queryset = queryset.filter(organization_id=organization)
        
        # Paginación
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Acceso de desarrollador autorizado',
            'total_records': queryset.count(),
            'results': serializer.data
        })
