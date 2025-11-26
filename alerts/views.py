from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alert
from .serializers import AlertSerializer
from .alert_service import AlertService
from .harvest_optimizer import HarvestOptimizer


class AlertViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de alertas"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = AlertSerializer
    
    def get_queryset(self):
        """Filtrar alertas por organización"""
        user = self.request.user
        if hasattr(user, 'partner') and user.partner:
            return Alert.objects.filter(
                organization=user.partner.organization,
                is_active=True
            )
        elif user.is_staff or user.is_superuser:
            from tenants.models import Organization
            org = Organization.objects.first()
            if org:
                return Alert.objects.filter(organization=org, is_active=True)
        return Alert.objects.none()
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Genera nuevas alertas automáticamente"""
        try:
            user = request.user
            organization = None
            
            if hasattr(user, 'partner') and user.partner:
                organization = user.partner.organization
            elif user.is_staff or user.is_superuser:
                from tenants.models import Organization
                organization = Organization.objects.first()
            
            if not organization:
                return Response(
                    {'error': 'Usuario no asociado a una organización'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = AlertService(organization)
            alerts = service.generate_all_alerts()
            
            serializer = self.get_serializer(alerts, many=True)
            
            return Response({
                'success': True,
                'message': f'{len(alerts)} alertas generadas',
                'alerts': serializer.data
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Marca una alerta como leída"""
        alert = self.get_object()
        alert.is_read = True
        alert.save()
        
        return Response({
            'success': True,
            'message': 'Alerta marcada como leída'
        })
    
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Desactiva una alerta"""
        alert = self.get_object()
        alert.is_active = False
        alert.save()
        
        return Response({
            'success': True,
            'message': 'Alerta desactivada'
        })
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Cuenta alertas no leídas"""
        count = self.get_queryset().filter(is_read=False).count()
        
        return Response({
            'count': count
        })
    
    @action(detail=False, methods=['get'])
    def optimal_harvest(self, request):
        """Calcula momento óptimo de cosecha para todas las parcelas"""
        try:
            user = request.user
            organization = None
            
            if hasattr(user, 'partner') and user.partner:
                organization = user.partner.organization
            elif user.is_staff or user.is_superuser:
                from tenants.models import Organization
                organization = Organization.objects.first()
            
            if not organization:
                return Response(
                    {'error': 'Usuario no asociado a una organización'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            optimizer = HarvestOptimizer(organization)
            results = optimizer.calculate_all_parcels()
            
            return Response({
                'success': True,
                'results': results,
                'count': len(results)
            })
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='optimal_harvest/(?P<parcel_id>[^/.]+)')
    def optimal_harvest_parcel(self, request, parcel_id=None):
        """Calcula momento óptimo de cosecha para una parcela específica"""
        try:
            from parcels.models import Parcel
            
            user = request.user
            organization = None
            
            if hasattr(user, 'partner') and user.partner:
                organization = user.partner.organization
            elif user.is_staff or user.is_superuser:
                from tenants.models import Organization
                organization = Organization.objects.first()
            
            if not organization:
                return Response(
                    {'error': 'Usuario no asociado a una organización'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            parcel = Parcel.objects.get(id=parcel_id, organization=organization)
            
            optimizer = HarvestOptimizer(organization)
            result = optimizer.calculate_optimal_harvest(parcel)
            
            return Response({
                'success': True,
                'result': result
            })
        
        except Parcel.DoesNotExist:
            return Response(
                {'error': 'Parcela no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
