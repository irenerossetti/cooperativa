from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from .models import RequestType, PartnerRequest, RequestItem
from .serializers import RequestTypeSerializer, PartnerRequestSerializer, RequestItemSerializer


class RequestTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RequestType.objects.filter(is_active=True)
    serializer_class = RequestTypeSerializer
    permission_classes = [IsAuthenticated]


class PartnerRequestViewSet(viewsets.ModelViewSet):
    queryset = PartnerRequest.objects.select_related('partner', 'request_type', 'assigned_to')
    serializer_class = PartnerRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        partner = self.request.query_params.get('partner', None)
        status_filter = self.request.query_params.get('status', None)
        request_type = self.request.query_params.get('request_type', None)
        priority = self.request.query_params.get('priority', None)
        
        if partner:
            queryset = queryset.filter(partner_id=partner)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if request_type:
            queryset = queryset.filter(request_type_id=request_type)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        partner_request = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        partner_request.assigned_to_id = user_id
        partner_request.status = PartnerRequest.IN_REVIEW
        partner_request.save()
        
        return Response({'message': 'Solicitud asignada exitosamente'})
    
    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        partner_request = self.get_object()
        response_text = request.data.get('response')
        
        if not response_text:
            return Response({'error': 'response es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        partner_request.response = response_text
        partner_request.response_date = timezone.now()
        partner_request.responded_by = request.user
        partner_request.save()
        
        return Response({'message': 'Respuesta registrada exitosamente'})
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        partner_request = self.get_object()
        partner_request.status = PartnerRequest.APPROVED
        partner_request.save()
        return Response({'message': 'Solicitud aprobada'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        partner_request = self.get_object()
        partner_request.status = PartnerRequest.REJECTED
        partner_request.save()
        return Response({'message': 'Solicitud rechazada'})
    
    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        if hasattr(request.user, 'partner'):
            requests = self.queryset.filter(partner=request.user.partner)
            serializer = self.get_serializer(requests, many=True)
            return Response(serializer.data)
        return Response({'error': 'Usuario no es un socio'}, status=status.HTTP_400_BAD_REQUEST)
