from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Sum
from .models import Partner, Community
from .serializers import PartnerSerializer, PartnerListSerializer, CommunitySerializer
from users.permissions import IsAdmin, IsAdminOrReadOnly
from audit.mixins import AuditMixin
from audit.models import AuditLog


class CommunityViewSet(AuditMixin, viewsets.ModelViewSet):
    """ViewSet para gestión de comunidades"""
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    audit_model_name = 'Community'
    
    def get_queryset(self):
        queryset = Community.objects.annotate(partners_count=Count('partners'))
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset


class PartnerViewSet(AuditMixin, viewsets.ModelViewSet):
    """ViewSet para gestión de socios"""
    queryset = Partner.objects.select_related('community', 'user')
    # Permitir a usuarios autenticados crear/editar socios
    # En producción, cambiar a IsAdminOrReadOnly si solo admins deben crear
    permission_classes = [IsAuthenticated]
    audit_model_name = 'Partner'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PartnerListSerializer
        return PartnerSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        search = self.request.query_params.get('search', None)
        community = self.request.query_params.get('community', None)
        status_filter = self.request.query_params.get('status', None)
        
        if search:
            queryset = queryset.filter(
                Q(ci__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )
        
        if community:
            queryset = queryset.filter(community_id=community)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        # Debug: verificar organización
        print(f"DEBUG: Creating partner in organization: {self.request.organization}")
        instance = serializer.save(created_by=self.request.user)
        self.create_audit_log(AuditLog.CREATE, instance)
        return instance
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def deactivate(self, request, pk=None):
        """Inhabilitar socio"""
        partner = self.get_object()
        partner.status = Partner.INACTIVE
        partner.save()
        self.create_audit_log(
            AuditLog.UPDATE, 
            partner, 
            f"Desactivó socio: {self.get_object_description(partner)}"
        )
        return Response({'message': 'Socio desactivado exitosamente'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def activate(self, request, pk=None):
        """Reactivar socio"""
        partner = self.get_object()
        partner.status = Partner.ACTIVE
        partner.save()
        self.create_audit_log(
            AuditLog.UPDATE, 
            partner, 
            f"Activó socio: {self.get_object_description(partner)}"
        )
        return Response({'message': 'Socio activado exitosamente'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def suspend(self, request, pk=None):
        """Suspender socio"""
        partner = self.get_object()
        partner.status = Partner.SUSPENDED
        partner.save()
        return Response({'message': 'Socio suspendido exitosamente'})
