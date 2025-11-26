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
        
        try:
            # Obtener datos según el tipo de reporte
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
