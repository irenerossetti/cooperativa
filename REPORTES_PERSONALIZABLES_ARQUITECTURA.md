# 📊 Sistema de Reportes Personalizables - Arquitectura

## Resumen Ejecutivo

Sistema completo de generación de reportes personalizables que permite a los usuarios:
- ✅ Construir reportes visuales (drag & drop)
- ✅ Seleccionar columnas dinámicamente
- ✅ Aplicar filtros y ordenamiento
- ✅ Exportar a Excel, PDF, HTML, Email
- ✅ Guardar plantillas de reportes
- ✅ Programar reportes automáticos

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                  SISTEMA DE REPORTES                        │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│   FRONTEND       │
│  Report Builder  │  ← Constructor visual de reportes
└────────┬─────────┘
         │
         │ API REST
         ▼
┌────────────────────────────────────────────────────────────┐
│                    BACKEND                                 │
├────────────────────────────────────────────────────────────┤
│  1. Report Definition (Modelo)                             │
│     - Columnas seleccionadas                               │
│     - Filtros aplicados                                    │
│     - Ordenamiento                                         │
│     - Agrupaciones                                         │
│                                                            │
│  2. Query Builder (Lógica)                                 │
│     - Construye queries dinámicas                          │
│     - Aplica filtros                                       │
│     - Ejecuta agregaciones                                 │
│                                                            │
│  3. Export Engine (Exportación)                            │
│     - Excel (openpyxl)                                     │
│     - PDF (ReportLab)                                      │
│     - HTML (Templates)                                     │
│     - Email (SMTP)                                         │
└────────────────────────────────────────────────────────────┘
```

---

## 📦 Componentes a Implementar

### 1. Backend - Modelos

**Archivo:** `Backend/reports/models.py`

```python
from django.db import models
from tenants.models import TenantModel
from users.models import User

class ReportDefinition(TenantModel):
    """Definición de un reporte personalizable"""
    
    # Información básica
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Fuente de datos
    SOURCE_MODELS = [
        ('partners', 'Socios'),
        ('parcels', 'Parcelas'),
        ('orders', 'Pedidos'),
        ('products', 'Productos'),
        ('payments', 'Pagos'),
        ('farm_activities', 'Labores Agrícolas'),
        ('harvested_products', 'Productos Cosechados'),
    ]
    source_model = models.CharField(max_length=50, choices=SOURCE_MODELS)
    
    # Configuración del reporte
    columns = models.JSONField(default=list)  # ['name', 'ci', 'phone']
    filters = models.JSONField(default=dict)  # {'status': 'ACTIVE', 'date_from': '2025-01-01'}
    order_by = models.JSONField(default=list)  # ['-created_at', 'name']
    group_by = models.JSONField(default=list)  # ['community', 'status']
    
    # Agregaciones
    aggregations = models.JSONField(default=dict)  # {'total_sales': 'SUM', 'avg_price': 'AVG'}
    
    # Configuración de visualización
    chart_type = models.CharField(
        max_length=20,
        choices=[
            ('table', 'Tabla'),
            ('bar', 'Gráfico de Barras'),
            ('line', 'Gráfico de Líneas'),
            ('pie', 'Gráfico Circular'),
        ],
        default='table'
    )
    
    # Metadatos
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_created')
    is_public = models.BooleanField(default=False)  # Compartido con otros usuarios
    is_scheduled = models.BooleanField(default=False)  # Programado para envío automático
    schedule_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Diario'),
            ('weekly', 'Semanal'),
            ('monthly', 'Mensual'),
        ],
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_source_model_display()})"


class ReportExecution(TenantModel):
    """Historial de ejecuciones de reportes"""
    
    report = models.ForeignKey(ReportDefinition, on_delete=models.CASCADE)
    executed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Parámetros de ejecución
    filters_applied = models.JSONField(default=dict)
    
    # Resultados
    rows_count = models.IntegerField(default=0)
    execution_time_ms = models.IntegerField(default=0)
    
    # Archivo generado
    file_format = models.CharField(
        max_length=10,
        choices=[
            ('excel', 'Excel'),
            ('pdf', 'PDF'),
            ('html', 'HTML'),
            ('csv', 'CSV'),
        ]
    )
    file_path = models.CharField(max_length=500, blank=True)
    file_size_kb = models.IntegerField(default=0)
    
    executed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-executed_at']
```

---

### 2. Backend - Query Builder

**Archivo:** `Backend/reports/query_builder.py`

```python
from django.apps import apps
from django.db.models import Q, Count, Sum, Avg, Max, Min
import time

class ReportQueryBuilder:
    """Constructor dinámico de queries para reportes"""
    
    # Mapeo de modelos
    MODEL_MAPPING = {
        'partners': 'partners.Partner',
        'parcels': 'parcels.Parcel',
        'orders': 'sales.Order',
        'products': 'production.HarvestedProduct',
        'payments': 'sales.Payment',
        'farm_activities': 'farm_activities.FarmActivity',
        'harvested_products': 'production.HarvestedProduct',
    }
    
    # Mapeo de columnas disponibles por modelo
    AVAILABLE_COLUMNS = {
        'partners': {
            'id': 'ID',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'ci': 'CI',
            'phone': 'Teléfono',
            'email': 'Email',
            'community__name': 'Comunidad',
            'status': 'Estado',
            'created_at': 'Fecha de Registro',
        },
        'orders': {
            'id': 'ID',
            'order_number': 'Número de Pedido',
            'customer__name': 'Cliente',
            'order_date': 'Fecha',
            'total': 'Total',
            'status': 'Estado',
            'campaign__name': 'Campaña',
        },
        'products': {
            'id': 'ID',
            'product_name': 'Producto',
            'quantity': 'Cantidad',
            'unit': 'Unidad',
            'harvest_date': 'Fecha de Cosecha',
            'parcel__name': 'Parcela',
            'campaign__name': 'Campaña',
        },
        # ... más modelos
    }
    
    # Operadores de filtro
    FILTER_OPERATORS = {
        'equals': '',
        'contains': '__icontains',
        'starts_with': '__istartswith',
        'ends_with': '__iendswith',
        'gt': '__gt',
        'gte': '__gte',
        'lt': '__lt',
        'lte': '__lte',
        'in': '__in',
        'between': '__range',
    }
    
    def __init__(self, report_definition):
        self.report = report_definition
        self.model = self._get_model()
    
    def _get_model(self):
        """Obtener el modelo Django desde el string"""
        model_path = self.MODEL_MAPPING.get(self.report.source_model)
        if not model_path:
            raise ValueError(f"Modelo no soportado: {self.report.source_model}")
        
        app_label, model_name = model_path.split('.')
        return apps.get_model(app_label, model_name)
    
    def build_query(self, additional_filters=None):
        """Construir query dinámica basada en la definición del reporte"""
        start_time = time.time()
        
        # Iniciar queryset
        queryset = self.model.objects.all()
        
        # Aplicar filtros de la definición
        queryset = self._apply_filters(queryset, self.report.filters)
        
        # Aplicar filtros adicionales (del usuario en tiempo de ejecución)
        if additional_filters:
            queryset = self._apply_filters(queryset, additional_filters)
        
        # Seleccionar columnas
        if self.report.columns:
            queryset = queryset.values(*self.report.columns)
        
        # Aplicar agrupación
        if self.report.group_by:
            queryset = self._apply_grouping(queryset)
        
        # Aplicar ordenamiento
        if self.report.order_by:
            queryset = queryset.order_by(*self.report.order_by)
        
        # Calcular tiempo de ejecución
        execution_time = int((time.time() - start_time) * 1000)
        
        return queryset, execution_time
    
    def _apply_filters(self, queryset, filters):
        """Aplicar filtros dinámicos"""
        q_objects = Q()
        
        for field, filter_config in filters.items():
            if isinstance(filter_config, dict):
                operator = filter_config.get('operator', 'equals')
                value = filter_config.get('value')
                
                # Construir el lookup
                lookup = field + self.FILTER_OPERATORS.get(operator, '')
                q_objects &= Q(**{lookup: value})
            else:
                # Filtro simple (valor directo)
                q_objects &= Q(**{field: filter_config})
        
        return queryset.filter(q_objects)
    
    def _apply_grouping(self, queryset):
        """Aplicar agrupación y agregaciones"""
        # Agrupar por campos
        queryset = queryset.values(*self.report.group_by)
        
        # Aplicar agregaciones
        aggregations = {}
        for field, agg_type in self.report.aggregations.items():
            if agg_type == 'COUNT':
                aggregations[f'{field}_count'] = Count(field)
            elif agg_type == 'SUM':
                aggregations[f'{field}_sum'] = Sum(field)
            elif agg_type == 'AVG':
                aggregations[f'{field}_avg'] = Avg(field)
            elif agg_type == 'MAX':
                aggregations[f'{field}_max'] = Max(field)
            elif agg_type == 'MIN':
                aggregations[f'{field}_min'] = Min(field)
        
        if aggregations:
            queryset = queryset.annotate(**aggregations)
        
        return queryset
    
    def get_available_columns(self):
        """Obtener columnas disponibles para el modelo"""
        return self.AVAILABLE_COLUMNS.get(self.report.source_model, {})
```

---

### 3. Backend - Export Engine

**Archivo:** `Backend/reports/exporters.py`

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import csv
from io import BytesIO, StringIO
import os

class ReportExporter:
    """Motor de exportación de reportes a múltiples formatos"""
    
    def __init__(self, report_definition, data, columns_labels):
        self.report = report_definition
        self.data = data
        self.columns_labels = columns_labels
    
    def export_to_excel(self):
        """Exportar a Excel (.xlsx)"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = self.report.name[:31]  # Excel limita a 31 caracteres
        
        # Estilos
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        # Escribir encabezados
        for col_idx, (field, label) in enumerate(self.columns_labels.items(), 1):
            cell = ws.cell(row=1, column=col_idx, value=label)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
        
        # Escribir datos
        for row_idx, row_data in enumerate(self.data, 2):
            for col_idx, field in enumerate(self.columns_labels.keys(), 1):
                value = row_data.get(field, '')
                ws.cell(row=row_idx, column=col_idx, value=value)
        
        # Ajustar ancho de columnas
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Guardar archivo
        file_path = self._get_file_path('xlsx')
        wb.save(file_path)
        
        return file_path
    
    def export_to_pdf(self):
        """Exportar a PDF"""
        file_path = self._get_file_path('pdf')
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title = Paragraph(f"<b>{self.report.name}</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Preparar datos para la tabla
        table_data = []
        
        # Encabezados
        headers = list(self.columns_labels.values())
        table_data.append(headers)
        
        # Datos
        for row in self.data:
            row_values = [str(row.get(field, '')) for field in self.columns_labels.keys()]
            table_data.append(row_values)
        
        # Crear tabla
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        elements.append(table)
        
        # Generar PDF
        doc.build(elements)
        
        return file_path
    
    def export_to_html(self):
        """Exportar a HTML"""
        context = {
            'report': self.report,
            'columns': self.columns_labels,
            'data': self.data,
            'total_rows': len(self.data),
        }
        
        html_content = render_to_string('reports/report_template.html', context)
        
        file_path = self._get_file_path('html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return file_path
    
    def export_to_csv(self):
        """Exportar a CSV"""
        file_path = self._get_file_path('csv')
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.columns_labels.keys())
            
            # Escribir encabezados con labels
            writer.writerow(self.columns_labels)
            
            # Escribir datos
            writer.writerows(self.data)
        
        return file_path
    
    def send_by_email(self, recipients, file_format='pdf'):
        """Enviar reporte por email"""
        # Generar archivo según formato
        if file_format == 'excel':
            file_path = self.export_to_excel()
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif file_format == 'pdf':
            file_path = self.export_to_pdf()
            mime_type = 'application/pdf'
        elif file_format == 'html':
            file_path = self.export_to_html()
            mime_type = 'text/html'
        else:
            file_path = self.export_to_csv()
            mime_type = 'text/csv'
        
        # Crear email
        subject = f"Reporte: {self.report.name}"
        body = f"""
        Estimado usuario,
        
        Adjunto encontrará el reporte "{self.report.name}" solicitado.
        
        Total de registros: {len(self.data)}
        Fecha de generación: {timezone.now().strftime('%d/%m/%Y %H:%M')}
        
        Saludos cordiales,
        Sistema de Gestión Cooperativa
        """
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )
        
        # Adjuntar archivo
        with open(file_path, 'rb') as f:
            email.attach(
                filename=os.path.basename(file_path),
                content=f.read(),
                mimetype=mime_type
            )
        
        email.send()
        
        return file_path
    
    def _get_file_path(self, extension):
        """Generar ruta de archivo"""
        from django.utils import timezone
        
        # Crear directorio si no existe
        reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generar nombre de archivo
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.report.name}_{timestamp}.{extension}"
        filename = filename.replace(' ', '_').replace('/', '_')
        
        return os.path.join(reports_dir, filename)
```

---

### 4. Backend - Views (API)

**Archivo:** `Backend/reports/views.py`

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from .models import ReportDefinition, ReportExecution
from .serializers import ReportDefinitionSerializer, ReportExecutionSerializer
from .query_builder import ReportQueryBuilder
from .exporters import ReportExporter
import os

class ReportDefinitionViewSet(viewsets.ModelViewSet):
    """ViewSet para definiciones de reportes"""
    serializer_class = ReportDefinitionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Reportes propios o públicos
        return ReportDefinition.objects.filter(
            models.Q(created_by=self.request.user) | 
            models.Q(is_public=True)
        )
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Ejecutar reporte y generar datos"""
        report = self.get_object()
        
        # Obtener filtros adicionales del request
        additional_filters = request.data.get('filters', {})
        
        # Construir query
        builder = ReportQueryBuilder(report)
        queryset, execution_time = builder.build_query(additional_filters)
        
        # Obtener datos
        data = list(queryset)
        
        # Obtener labels de columnas
        columns_labels = builder.get_available_columns()
        selected_labels = {
            col: columns_labels.get(col, col) 
            for col in report.columns
        }
        
        return Response({
            'data': data,
            'columns': selected_labels,
            'total_rows': len(data),
            'execution_time_ms': execution_time,
        })
    
    @action(detail=True, methods=['post'])
    def export(self, request, pk=None):
        """Exportar reporte a formato específico"""
        report = self.get_object()
        file_format = request.data.get('format', 'excel')  # excel, pdf, html, csv
        
        # Ejecutar reporte
        builder = ReportQueryBuilder(report)
        queryset, execution_time = builder.build_query(request.data.get('filters', {}))
        data = list(queryset)
        
        # Obtener labels
        columns_labels = builder.get_available_columns()
        selected_labels = {
            col: columns_labels.get(col, col) 
            for col in report.columns
        }
        
        # Exportar
        exporter = ReportExporter(report, data, selected_labels)
        
        if file_format == 'excel':
            file_path = exporter.export_to_excel()
        elif file_format == 'pdf':
            file_path = exporter.export_to_pdf()
        elif file_format == 'html':
            file_path = exporter.export_to_html()
        else:
            file_path = exporter.export_to_csv()
        
        # Registrar ejecución
        ReportExecution.objects.create(
            report=report,
            executed_by=request.user,
            filters_applied=request.data.get('filters', {}),
            rows_count=len(data),
            execution_time_ms=execution_time,
            file_format=file_format,
            file_path=file_path,
            file_size_kb=os.path.getsize(file_path) // 1024
        )
        
        # Devolver archivo
        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(file_path)
        )
    
    @action(detail=True, methods=['post'])
    def send_email(self, request, pk=None):
        """Enviar reporte por email"""
        report = self.get_object()
        recipients = request.data.get('recipients', [])
        file_format = request.data.get('format', 'pdf')
        
        if not recipients:
            return Response(
                {'error': 'Se requiere al menos un destinatario'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ejecutar reporte
        builder = ReportQueryBuilder(report)
        queryset, _ = builder.build_query(request.data.get('filters', {}))
        data = list(queryset)
        
        # Obtener labels
        columns_labels = builder.get_available_columns()
        selected_labels = {
            col: columns_labels.get(col, col) 
            for col in report.columns
        }
        
        # Enviar por email
        exporter = ReportExporter(report, data, selected_labels)
        file_path = exporter.send_by_email(recipients, file_format)
        
        return Response({
            'message': f'Reporte enviado a {len(recipients)} destinatario(s)',
            'recipients': recipients
        })
    
    @action(detail=True, methods=['get'])
    def available_columns(self, request, pk=None):
        """Obtener columnas disponibles para el modelo del reporte"""
        report = self.get_object()
        builder = ReportQueryBuilder(report)
        columns = builder.get_available_columns()
        
        return Response({
            'model': report.source_model,
            'columns': columns
        })
```

---

## 📝 Continuará en el siguiente archivo...

Este es el primer archivo de la arquitectura. ¿Quieres que continúe con:
1. Frontend - Constructor visual de reportes
2. Instalación de dependencias
3. Ejemplos de uso
4. Documentación completa

?
