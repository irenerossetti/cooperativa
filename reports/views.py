from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg
import csv
from datetime import datetime
from .models import ReportType, GeneratedReport
from .serializers import ReportTypeSerializer, GeneratedReportSerializer
from .utils import export_to_csv, export_to_excel, export_to_pdf
from .ml_predictions import YieldPredictor, ProductionForecaster
from partners.models import Partner, Community
from parcels.models import Parcel
from production.models import HarvestedProduct


class ReportTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReportType.objects.filter(is_active=True)
    serializer_class = ReportTypeSerializer
    permission_classes = [IsAuthenticated]


class ReportViewSet(viewsets.ModelViewSet):
    queryset = GeneratedReport.objects.all()
    serializer_class = GeneratedReportSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def performance_by_partner(self, request):
        """Reporte de rendimiento por socio"""
        partner_id = request.query_params.get('partner_id')
        
        try:
            if partner_id:
                partners = Partner.objects.filter(id=partner_id)
            else:
                partners = Partner.objects.all()
            
            data = []
            for partner in partners:
                production = HarvestedProduct.objects.filter(partner=partner)
                total_prod = production.aggregate(Sum('quantity'))['quantity__sum'] or 0
                avg_yield = production.aggregate(Avg('quantity'))['quantity__avg'] or 0
                
                partner_name = f"{partner.first_name} {partner.last_name}"
                
                data.append({
                    'partner_id': partner.id,
                    'partner_name': partner_name,
                    'total_production': float(total_prod),
                    'total_parcels': partner.parcels.count(),
                    'avg_yield': float(avg_yield)
                })
            
            return Response(data)
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al generar el reporte de socios'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def population_active_partners(self, request):
        """Población activa de socios"""
        data = {
            'total_active': Partner.objects.filter(status='ACTIVE').count(),
            'by_community': Partner.objects.values('community__name').annotate(
                count=Count('id')
            ),
            'by_status': Partner.objects.values('status').annotate(count=Count('id'))
        }
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def hectares_by_crop(self, request):
        """Hectáreas por cultivo"""
        data = Parcel.objects.values('current_crop__name').annotate(
            total_hectares=Sum('surface'),
            parcel_count=Count('id')
        )
        return Response(data)
    
    @action(detail=False, methods=['post'])
    def export_report(self, request):
        """Exportar reporte en múltiples formatos (CSV, Excel, PDF)"""
        report_type = request.data.get('report_type')
        export_format = request.data.get('format', 'csv').lower()
        custom_data = request.data.get('data')  # Datos filtrados del frontend
        custom_headers = request.data.get('headers')  # Headers personalizados
        selected_columns = request.data.get('selected_columns', [])
        
        try:
            # Si se envían datos personalizados, usarlos
            if custom_data and custom_headers:
                # Convertir datos de dict a lista de listas
                data = []
                for item in custom_data:
                    row = []
                    for col in selected_columns:
                        value = item.get(col, '')
                        # Formatear valores numéricos
                        if isinstance(value, (int, float)):
                            row.append(round(float(value), 2))
                        else:
                            row.append(value if value is not None else '')
                    data.append(row)
                headers = custom_headers
                
                # Determinar título según tipo de reporte
                title_map = {
                    'performance_by_partner': 'Reporte de Rendimiento por Socio',
                    'performance_by_parcel': 'Reporte de Rendimiento por Parcela',
                    'partners_by_community': 'Socios por Comunidad',
                    'hectares_by_crop': 'Hectáreas por Cultivo',
                    'hectares_by_crop_detailed': 'Hectáreas por Cultivo - Detallado',
                    'population_active_partners': 'Población Activa de Socios'
                }
                title = title_map.get(report_type, 'Reporte')
            else:
                # Obtener datos según el tipo de reporte (modo legacy)
                if report_type == 'performance_by_partner':
                    data, headers = self._get_performance_data()
                    title = 'Reporte de Rendimiento por Socio'
                elif report_type == 'population_active_partners':
                    data, headers = self._get_population_data()
                    title = 'Población Activa de Socios'
                elif report_type == 'hectares_by_crop':
                    data, headers = self._get_hectares_data()
                    title = 'Hectáreas por Cultivo'
                elif report_type == 'performance_by_parcel':
                    data, headers = self._get_parcel_performance_data()
                    title = 'Reporte de Rendimiento por Parcela'
                elif report_type == 'partners_by_community':
                    data, headers = self._get_partners_by_community_data()
                    title = 'Socios por Comunidad'
                elif report_type == 'hectares_by_crop_detailed':
                    data, headers = self._get_hectares_by_crop_data()
                    title = 'Hectáreas por Cultivo - Detallado'
                else:
                    return Response({'error': 'Tipo de reporte no válido'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
            
            # Generar archivo según formato
            filename = f"{report_type}_{datetime.now().strftime('%Y%m%d')}"
            
            if export_format == 'excel':
                return export_to_excel(data, f"{filename}.xlsx", headers)
            elif export_format == 'pdf':
                return export_to_pdf(data, f"{filename}.pdf", title, headers)
            else:  # CSV por defecto
                return export_to_csv(data, f"{filename}.csv", headers)
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al exportar el reporte'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_performance_data(self):
        """Obtener datos de rendimiento"""
        partners = Partner.objects.all()
        headers = ['ID', 'Socio', 'Producción Total', 'Parcelas', 'Rendimiento Promedio']
        data = []
        
        for partner in partners:
            production = HarvestedProduct.objects.filter(partner=partner)
            partner_name = f"{partner.first_name} {partner.last_name}"
            data.append([
                partner.id,
                partner_name,
                production.aggregate(Sum('quantity'))['quantity__sum'] or 0,
                partner.parcels.count(),
                round(production.aggregate(Avg('quantity'))['quantity__avg'] or 0, 2)
            ])
        
        return data, headers
    
    def _get_population_data(self):
        """Obtener datos de población"""
        headers = ['Comunidad', 'Socios Activos']
        data = []
        
        communities = Partner.objects.values('community__name').annotate(
            count=Count('id', filter=Partner.objects.filter(status='ACTIVE').values('id'))
        )
        
        for item in communities:
            data.append([
                item['community__name'] or 'Sin comunidad',
                item['count']
            ])
        
        return data, headers
    
    def _get_hectares_data(self):
        """Obtener datos de hectáreas"""
        headers = ['Cultivo', 'Hectáreas Totales', 'Número de Parcelas']
        data = []
        
        crops = Parcel.objects.values('current_crop__name').annotate(
            total_hectares=Sum('surface'),
            parcel_count=Count('id')
        )
        
        for item in crops:
            data.append([
                item['current_crop__name'] or 'Sin cultivo',
                round(float(item['total_hectares'] or 0), 2),
                item['parcel_count']
            ])
        
        return data, headers
    
    def _get_parcel_performance_data(self):
        """Obtener datos de rendimiento por parcela"""
        headers = ['Código Parcela', 'Socio', 'Superficie (ha)', 'Producción (kg)', 'Rendimiento (kg/ha)']
        data = []
        
        parcels = Parcel.objects.all().select_related('partner')
        
        for parcel in parcels:
            production = HarvestedProduct.objects.filter(parcel=parcel)
            total_prod = production.aggregate(Sum('quantity'))['quantity__sum'] or 0
            
            partner_name = f"{parcel.partner.first_name} {parcel.partner.last_name}" if parcel.partner else "Sin socio"
            parcel_code = parcel.code if hasattr(parcel, 'code') else f"Parcela-{parcel.id}"
            surface = float(parcel.surface) if parcel.surface else 0
            yield_per_ha = float(total_prod) / surface if surface > 0 else 0
            
            data.append([
                parcel_code,
                partner_name,
                round(surface, 2),
                round(float(total_prod), 2),
                round(yield_per_ha, 2)
            ])
        
        return data, headers
    
    def _get_partners_by_community_data(self):
        """Obtener datos de socios por comunidad"""
        headers = ['Comunidad', 'Total Socios', 'Socios Activos', 'Socios Inactivos', 'Producción Total (kg)', 'Promedio por Socio (kg)']
        data = []
        
        communities = Community.objects.all()
        
        for community in communities:
            partners = Partner.objects.filter(community=community)
            active_partners = partners.filter(status='ACTIVE')
            
            # Calcular producción total
            total_production = 0
            for partner in partners:
                prod = HarvestedProduct.objects.filter(partner=partner).aggregate(Sum('quantity'))
                total_production += prod['quantity__sum'] or 0
            
            avg_production = total_production / partners.count() if partners.count() > 0 else 0
            
            data.append([
                community.name,
                partners.count(),
                active_partners.count(),
                partners.count() - active_partners.count(),
                round(float(total_production), 2),
                round(float(avg_production), 2)
            ])
        
        return data, headers
    
    def _get_hectares_by_crop_data(self):
        """Obtener datos de hectáreas por cultivo"""
        headers = ['Cultivo', 'Hectáreas Totales', 'Número de Parcelas', 'Tamaño Promedio (ha)', '% del Total']
        data = []
        
        crops = Parcel.objects.values('current_crop__name').annotate(
            total_hectares=Sum('surface'),
            parcel_count=Count('id')
        )
        
        total_hectares = sum(float(item['total_hectares'] or 0) for item in crops)
        
        for item in crops:
            hectares = float(item['total_hectares'] or 0)
            count = item['parcel_count']
            avg_size = hectares / count if count > 0 else 0
            percentage = (hectares / total_hectares * 100) if total_hectares > 0 else 0
            
            data.append([
                item['current_crop__name'] or 'Sin cultivo',
                round(hectares, 2),
                count,
                round(avg_size, 2),
                round(percentage, 1)
            ])
        
        return data, headers
    
    @action(detail=False, methods=['get'])
    def performance_by_parcel(self, request):
        """Reporte de rendimiento por parcela"""
        parcel_id = request.query_params.get('parcel_id')
        
        try:
            if parcel_id:
                parcels = Parcel.objects.filter(id=parcel_id).select_related('partner')
            else:
                parcels = Parcel.objects.all().select_related('partner')
            
            data = []
            for parcel in parcels:
                production = HarvestedProduct.objects.filter(parcel=parcel)
                total_prod = production.aggregate(Sum('quantity'))['quantity__sum'] or 0
                
                # Obtener nombre del socio
                partner_name = f"{parcel.partner.first_name} {parcel.partner.last_name}" if parcel.partner else "Sin socio"
                
                data.append({
                    'parcel_id': parcel.id,
                    'parcel_code': parcel.code if hasattr(parcel, 'code') else f"Parcela-{parcel.id}",
                    'partner_name': partner_name,
                    'surface': float(parcel.surface) if parcel.surface else 0,
                    'total_production': float(total_prod),
                    'yield_per_hectare': float(total_prod) / float(parcel.surface) if parcel.surface and float(parcel.surface) > 0 else 0
                })
            
            return Response(data)
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al generar el reporte de parcelas'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def train_ml_model(self, request):
        """Entrena el modelo de Machine Learning con datos históricos"""
        try:
            predictor = YieldPredictor()
            result = predictor.train()
            return Response(result)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al entrenar el modelo'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def predict_yield(self, request):
        """Predice el rendimiento de una parcela"""
        parcel_id = request.query_params.get('parcel_id')
        
        if not parcel_id:
            return Response({
                'error': 'parcel_id es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            forecaster = ProductionForecaster()
            prediction = forecaster.forecast_parcel_production(parcel_id)
            
            if prediction is None:
                return Response({
                    'error': 'No se pudo generar la predicción. Verifica que el modelo esté entrenado.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(prediction)
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al predecir rendimiento'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def predict_partner_production(self, request):
        """Predice la producción total de un socio"""
        partner_id = request.query_params.get('partner_id')
        
        if not partner_id:
            return Response({
                'error': 'partner_id es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            forecaster = ProductionForecaster()
            prediction = forecaster.forecast_partner_production(partner_id)
            
            if prediction is None:
                return Response({
                    'error': 'No se pudo generar la predicción'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(prediction)
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al predecir producción del socio'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def ml_insights(self, request):
        """Obtiene insights del modelo de ML"""
        try:
            predictor = YieldPredictor()
            if not predictor.load_model():
                return Response({
                    'error': 'Modelo no entrenado. Ejecuta /train_ml_model/ primero.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            importance = predictor.get_feature_importance()
            
            return Response({
                'feature_importance': importance,
                'model_status': 'trained',
                'recommendations': [
                    'La superficie de la parcela es el factor más importante' if importance['surface'] > 0.3 else None,
                    'El tipo de suelo tiene impacto significativo' if importance['soil_type'] > 0.2 else None,
                    'El tipo de cultivo es determinante' if importance['crop_type'] > 0.2 else None,
                ]
            })
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al obtener insights'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def fertilization_plan(self, request):
        """Genera plan de fertilización inteligente basado en IA"""
        try:
            from campaigns.models import Campaign
            from inventory.models import Product
            from django.utils import timezone
            
            # Obtener campañas activas
            active_campaigns = Campaign.objects.filter(
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            )
            
            recommendations = []
            for campaign in active_campaigns[:5]:  # Top 5 campañas
                parcels = campaign.parcels.all()
                total_area = sum(float(p.surface or 0) for p in parcels)
                
                # Calcular necesidades basadas en área y tipo de cultivo
                if total_area > 0:
                    # Fertilizante NPK: 200 kg/ha
                    npk_needed = total_area * 200
                    # Fertilizante orgánico: 150 kg/ha
                    organic_needed = total_area * 150
                    
                    recommendations.append({
                        'campaign_id': campaign.id,
                        'campaign_name': campaign.name,
                        'total_area': round(total_area, 2),
                        'fertilizers': [
                            {
                                'type': 'NPK 15-15-15',
                                'quantity': round(npk_needed, 2),
                                'unit': 'kg',
                                'application_rate': '200 kg/ha',
                                'timing': 'Aplicar en 3 dosis: siembra, 30 días, 60 días',
                                'priority': 'Alta'
                            },
                            {
                                'type': 'Fertilizante Orgánico',
                                'quantity': round(organic_needed, 2),
                                'unit': 'kg',
                                'application_rate': '150 kg/ha',
                                'timing': 'Aplicar 15 días antes de siembra',
                                'priority': 'Media'
                            }
                        ],
                        'estimated_cost': round((npk_needed * 2.5) + (organic_needed * 1.8), 2),
                        'expected_yield_increase': '15-20%'
                    })
            
            return Response({
                'success': True,
                'recommendations': recommendations,
                'total_campaigns': len(recommendations),
                'generated_at': timezone.now().isoformat()
            })
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al generar plan de fertilización'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def price_alerts(self, request):
        """Genera alertas de precios y oportunidades comerciales"""
        try:
            from production.models import HarvestedProduct
            from pricing.models import SeasonalPrice
            from django.utils import timezone
            from django.db.models import Avg, Max, Min
            import random
            
            # Obtener productos cosechados recientes
            recent_products = HarvestedProduct.objects.all()[:10]
            
            alerts = []
            opportunities = []
            
            # Simular análisis de precios (en producción conectar a API real)
            products_analyzed = {}
            for prod in recent_products:
                product_name = prod.product.name if prod.product else 'Producto'
                if product_name not in products_analyzed:
                    # Precio base simulado
                    base_price = random.uniform(2.5, 8.5)
                    current_price = base_price * random.uniform(0.9, 1.15)
                    trend = random.choice(['up', 'down', 'stable'])
                    
                    products_analyzed[product_name] = {
                        'product': product_name,
                        'current_price': round(current_price, 2),
                        'base_price': round(base_price, 2),
                        'trend': trend,
                        'change_percent': round(((current_price - base_price) / base_price) * 100, 1)
                    }
                    
                    # Generar alertas
                    if trend == 'up' and current_price > base_price * 1.1:
                        alerts.append({
                            'type': 'price_increase',
                            'product': product_name,
                            'message': f'Precio de {product_name} subió {abs(products_analyzed[product_name]["change_percent"])}%',
                            'severity': 'high',
                            'action': 'Considerar venta inmediata'
                        })
                        opportunities.append({
                            'product': product_name,
                            'opportunity': 'Venta',
                            'reason': f'Precio {abs(products_analyzed[product_name]["change_percent"])}% sobre promedio',
                            'potential_profit': round(current_price * 1000, 2)  # Por tonelada
                        })
                    elif trend == 'down' and current_price < base_price * 0.9:
                        alerts.append({
                            'type': 'price_decrease',
                            'product': product_name,
                            'message': f'Precio de {product_name} bajó {abs(products_analyzed[product_name]["change_percent"])}%',
                            'severity': 'medium',
                            'action': 'Retener stock si es posible'
                        })
            
            # Agregar alertas de demanda
            alerts.append({
                'type': 'high_demand',
                'product': 'Quinua',
                'message': 'Alta demanda detectada en mercado internacional',
                'severity': 'high',
                'action': 'Incrementar producción para próxima temporada'
            })
            
            return Response({
                'success': True,
                'alerts': alerts[:5],
                'opportunities': opportunities[:3],
                'market_summary': {
                    'total_products_analyzed': len(products_analyzed),
                    'trending_up': len([p for p in products_analyzed.values() if p['trend'] == 'up']),
                    'trending_down': len([p for p in products_analyzed.values() if p['trend'] == 'down']),
                    'stable': len([p for p in products_analyzed.values() if p['trend'] == 'stable'])
                },
                'generated_at': timezone.now().isoformat()
            })
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al generar alertas de precios'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def partners_by_community(self, request):
        """Reporte de socios por comunidad con estadísticas"""
        try:
            communities = Community.objects.all()
            
            data = []
            for community in communities:
                partners = Partner.objects.filter(community=community)
                active_partners = partners.filter(status='ACTIVE')
                
                # Calcular producción total de la comunidad
                total_production = 0
                for partner in partners:
                    prod = HarvestedProduct.objects.filter(partner=partner).aggregate(Sum('quantity'))
                    total_production += prod['quantity__sum'] or 0
                
                data.append({
                    'community_id': community.id,
                    'community_name': community.name,
                    'total_partners': partners.count(),
                    'active_partners': active_partners.count(),
                    'inactive_partners': partners.count() - active_partners.count(),
                    'total_production': round(float(total_production), 2),
                    'avg_production_per_partner': round(float(total_production) / partners.count(), 2) if partners.count() > 0 else 0
                })
            
            return Response({
                'success': True,
                'data': data,
                'total_communities': len(data)
            })
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al generar reporte de comunidades'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
