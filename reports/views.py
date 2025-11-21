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
        
        if partner_id:
            partners = Partner.objects.filter(id=partner_id)
        else:
            partners = Partner.objects.all()
        
        data = []
        for partner in partners:
            production = HarvestedProduct.objects.filter(partner=partner)
            data.append({
                'partner_id': partner.id,
                'partner_name': partner.full_name,
                'total_production': production.aggregate(Sum('quantity'))['quantity__sum'] or 0,
                'total_parcels': partner.parcels.count(),
                'avg_yield': production.aggregate(Avg('quantity'))['quantity__avg'] or 0
            })
        
        return Response(data)
    
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
    
    def _get_performance_data(self):
        """Obtener datos de rendimiento"""
        partners = Partner.objects.all()
        headers = ['ID', 'Socio', 'Producción Total', 'Parcelas', 'Rendimiento Promedio']
        data = []
        
        for partner in partners:
            production = HarvestedProduct.objects.filter(partner=partner)
            data.append([
                partner.id,
                partner.full_name,
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
    
    @action(detail=False, methods=['get'])
    def performance_by_parcel(self, request):
        """Reporte de rendimiento por parcela"""
        parcel_id = request.query_params.get('parcel_id')
        
        if parcel_id:
            parcels = Parcel.objects.filter(id=parcel_id)
        else:
            parcels = Parcel.objects.all()
        
        data = []
        for parcel in parcels:
            production = HarvestedProduct.objects.filter(parcel=parcel)
            data.append({
                'parcel_id': parcel.id,
                'parcel_code': parcel.code,
                'partner_name': parcel.partner.full_name,
                'surface': float(parcel.surface),
                'total_production': production.aggregate(Sum('quantity'))['quantity__sum'] or 0,
                'yield_per_hectare': (production.aggregate(Sum('quantity'))['quantity__sum'] or 0) / float(parcel.surface) if parcel.surface > 0 else 0
            })
        
        return Response(data)
