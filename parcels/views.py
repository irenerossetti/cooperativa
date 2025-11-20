from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Parcel, SoilType, Crop
from .serializers import (ParcelSerializer, ParcelListSerializer, 
                          SoilTypeSerializer, CropSerializer)
from users.permissions import IsAdminOrReadOnly


class SoilTypeViewSet(viewsets.ModelViewSet):
    """ViewSet para tipos de suelo"""
    queryset = SoilType.objects.all()
    serializer_class = SoilTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class CropViewSet(viewsets.ModelViewSet):
    """ViewSet para cultivos"""
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class ParcelViewSet(viewsets.ModelViewSet):
    """ViewSet para parcelas"""
    queryset = Parcel.objects.select_related('partner', 'soil_type', 'current_crop')
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ParcelListSerializer
        return ParcelSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        partner = self.request.query_params.get('partner', None)
        soil_type = self.request.query_params.get('soil_type', None)
        crop = self.request.query_params.get('crop', None)
        status_filter = self.request.query_params.get('status', None)
        search = self.request.query_params.get('search', None)
        
        if partner:
            queryset = queryset.filter(partner_id=partner)
        
        if soil_type:
            queryset = queryset.filter(soil_type_id=soil_type)
        
        if crop:
            queryset = queryset.filter(current_crop_id=crop)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(name__icontains=search) |
                Q(location__icontains=search)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
