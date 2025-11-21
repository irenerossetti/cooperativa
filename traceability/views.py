from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ParcelTraceability, InputUsageRecord
from .serializers import ParcelTraceabilitySerializer, InputUsageRecordSerializer


class ParcelTraceabilityViewSet(viewsets.ModelViewSet):
    queryset = ParcelTraceability.objects.select_related('parcel', 'campaign')
    serializer_class = ParcelTraceabilitySerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def full_history(self, request, pk=None):
        """Historial completo de trazabilidad"""
        traceability = self.get_object()
        
        data = {
            'traceability': self.get_serializer(traceability).data,
            'input_records': InputUsageRecordSerializer(
                traceability.input_records.all(), many=True
            ).data,
            'activities': traceability.parcel.activities.filter(
                campaign=traceability.campaign
            ).count()
        }
        return Response(data)


class InputUsageRecordViewSet(viewsets.ModelViewSet):
    queryset = InputUsageRecord.objects.select_related('traceability', 'inventory_item')
    serializer_class = InputUsageRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)
