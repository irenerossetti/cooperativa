from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MarketPrice, PriceAlert
from .serializers import MarketPriceSerializer, PriceAlertSerializer
from .market_service import MarketAnalysisService


class MarketAnalysisViewSet(viewsets.ViewSet):
    """ViewSet para análisis de mercado"""
    
    permission_classes = [IsAuthenticated]
    
    def _get_organization(self, user):
        """Helper para obtener organización del usuario"""
        if hasattr(user, 'partner') and user.partner:
            return user.partner.organization
        elif user.is_staff or user.is_superuser:
            from tenants.models import Organization
            return Organization.objects.first()
        return None
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Obtiene tendencias de precios de mercado"""
        try:
            organization = self._get_organization(request.user)
            if not organization:
                return Response({
                    'success': True,
                    'trends': [],
                    'count': 0
                })
            
            service = MarketAnalysisService(organization)
            trends = service.get_market_trends()
            
            return Response({
                'success': True,
                'trends': trends,
                'count': len(trends)
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """Obtiene alertas de precio activas"""
        try:
            organization = self._get_organization(request.user)
            if not organization:
                return Response({
                    'success': True,
                    'alerts': [],
                    'count': 0
                })
            
            service = MarketAnalysisService(organization)
            alerts = service.get_price_alerts()
            
            return Response({
                'success': True,
                'alerts': alerts,
                'count': len(alerts)
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def opportunities(self, request):
        """Detecta oportunidades comerciales"""
        try:
            organization = self._get_organization(request.user)
            if not organization:
                return Response({
                    'success': True,
                    'opportunities': [],
                    'count': 0
                })
            
            service = MarketAnalysisService(organization)
            opportunities = service.get_opportunities()
            
            return Response({
                'success': True,
                'opportunities': opportunities,
                'count': len(opportunities)
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def demand(self, request):
        """Análisis de demanda de productos"""
        try:
            organization = self._get_organization(request.user)
            if not organization:
                return Response({
                    'success': True,
                    'demand': [],
                    'count': 0
                })
            
            service = MarketAnalysisService(organization)
            demand = service.get_demand_analysis()
            
            return Response({
                'success': True,
                'demand': demand,
                'count': len(demand)
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Resumen completo del análisis de mercado"""
        try:
            organization = self._get_organization(request.user)
            
            # Si no hay organización, devolver datos vacíos
            if not organization:
                return Response({
                    'success': True,
                    'data': {
                        'trends': [],
                        'alerts': [],
                        'opportunities': [],
                        'demand_analysis': [],
                        'last_updated': datetime.now().isoformat(),
                        'total_products_tracked': 0
                    }
                })
            
            service = MarketAnalysisService(organization)
            summary = service.get_market_summary()
            
            return Response({
                'success': True,
                'data': summary
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MarketPriceViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de precios de mercado"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = MarketPriceSerializer
    
    def get_queryset(self):
        organization = self.request.user.partner.organization if hasattr(self.request.user, 'partner') else None
        if organization:
            return MarketPrice.objects.filter(organization=organization)
        return MarketPrice.objects.none()


class PriceAlertViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de alertas de precio"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = PriceAlertSerializer
    
    def get_queryset(self):
        organization = self.request.user.partner.organization if hasattr(self.request.user, 'partner') else None
        if organization:
            return PriceAlert.objects.filter(organization=organization, is_active=True)
        return PriceAlert.objects.none()
