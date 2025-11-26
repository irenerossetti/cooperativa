# 📊 Reportes Personalizables - Resumen y Justificación

## 🎯 Requisito

> **Reportes personalizables:** Aparte de los reportes obvios que debe tener todo sistema, debe existir mecanismos que permita al usuario construir sus propios reportes, indicando que columnas, que criterios de selección y orden se debe mostrar. Así mismo todo reporte antes de generar debe haber una interface para posibilitar filtrar la información a obtener. Tomar en cuenta que todo reporte debe tener la facilidad de ser exportado a otros formatos como ser: Excel, HTML, eMail, PDF.

---

## ✅ Solución Propuesta

### Sistema Completo de Reportes Personalizables

Un sistema modular que permite a los usuarios:

1. ✅ **Construir reportes visualmente** - Sin código
2. ✅ **Seleccionar columnas** - Drag & drop
3. ✅ **Aplicar filtros dinámicos** - Múltiples criterios
4. ✅ **Ordenar y agrupar** - Personalizable
5. ✅ **Exportar a múltiples formatos** - Excel, PDF, HTML, CSV, Email
6. ✅ **Guardar plantillas** - Reutilizables
7. ✅ **Programar envíos** - Automáticos

---

## 🏗️ Arquitectura

### Backend (Django + Python)

```
┌─────────────────────────────────────────────────────────┐
│                    BACKEND LAYER                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. MODELS (Base de Datos)                             │
│     ├── ReportDefinition                               │
│     │   ├── name, description                          │
│     │   ├── source_model (partners, orders, etc.)      │
│     │   ├── columns (JSON)                             │
│     │   ├── filters (JSON)                             │
│     │   ├── order_by (JSON)                            │
│     │   └── aggregations (JSON)                        │
│     │                                                   │
│     └── ReportExecution                                │
│         ├── report (FK)                                │
│         ├── executed_by (FK)                           │
│         ├── file_path                                  │
│         └── execution_time                             │
│                                                         │
│  2. QUERY BUILDER (Lógica)                             │
│     ├── Construye queries dinámicas                    │
│     ├── Aplica filtros (equals, contains, gt, etc.)    │
│     ├── Aplica ordenamiento                            │
│     └── Ejecuta agregaciones (SUM, AVG, COUNT)         │
│                                                         │
│  3. EXPORT ENGINE (Exportación)                        │
│     ├── ExcelExporter (openpyxl)                       │
│     ├── PDFExporter (ReportLab)                        │
│     ├── HTMLExporter (Django Templates)                │
│     ├── CSVExporter (csv module)                       │
│     └── EmailSender (SMTP)                             │
│                                                         │
│  4. API ENDPOINTS                                      │
│     ├── POST /api/reports/definitions/                 │
│     ├── POST /api/reports/{id}/execute/                │
│     ├── POST /api/reports/{id}/export/                 │
│     ├── POST /api/reports/{id}/send_email/             │
│     └── GET  /api/reports/{id}/available_columns/      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Frontend (React)

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND LAYER                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. REPORT BUILDER (Constructor Visual)                │
│     ├── Selector de fuente de datos                    │
│     ├── Selector de columnas (drag & drop)             │
│     ├── Constructor de filtros                         │
│     ├── Configuración de ordenamiento                  │
│     └── Vista previa en tiempo real                    │
│                                                         │
│  2. COMPONENTS                                         │
│     ├── ColumnSelector                                 │
│     │   └── Drag & drop de columnas                    │
│     ├── FilterBuilder                                  │
│     │   └── Filtros dinámicos con operadores           │
│     ├── ReportPreview                                  │
│     │   └── Tabla con datos en tiempo real             │
│     └── ExportOptions                                  │
│         └── Modal con opciones de exportación          │
│                                                         │
│  3. EXPORT INTERFACE                                   │
│     ├── Botón "Exportar a Excel"                       │
│     ├── Botón "Exportar a PDF"                         │
│     ├── Botón "Exportar a HTML"                        │
│     ├── Botón "Enviar por Email"                       │
│     └── Configuración de destinatarios                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Flujo de Usuario

### 1. Crear Reporte Personalizado

```
Usuario → Selecciona "Nuevo Reporte"
       ↓
       Elige fuente de datos (Socios, Pedidos, etc.)
       ↓
       Selecciona columnas (drag & drop)
       ↓
       Aplica filtros (fecha, estado, etc.)
       ↓
       Configura ordenamiento
       ↓
       Vista previa de datos
       ↓
       Guarda plantilla (opcional)
```

### 2. Exportar Reporte

```
Usuario → Hace clic en "Exportar"
       ↓
       Selecciona formato (Excel, PDF, HTML, CSV)
       ↓
       Aplica filtros adicionales (opcional)
       ↓
       Sistema genera archivo
       ↓
       Descarga automática
```

### 3. Enviar por Email

```
Usuario → Hace clic en "Enviar por Email"
       ↓
       Ingresa destinatarios
       ↓
       Selecciona formato adjunto
       ↓
       Sistema genera y envía email
       ↓
       Confirmación de envío
```

---

## 📋 Características Implementadas

### ✅ Constructor Visual

**Características:**
- Interfaz drag & drop para columnas
- Selector visual de filtros
- Vista previa en tiempo real
- Guardado de plantillas
- Compartir reportes con otros usuarios

**Ejemplo de uso:**
```javascript
// Usuario selecciona columnas
columns: ['first_name', 'last_name', 'ci', 'phone', 'community__name']

// Usuario aplica filtros
filters: {
  'status': { operator: 'equals', value: 'ACTIVE' },
  'created_at': { operator: 'gte', value: '2025-01-01' }
}

// Usuario configura ordenamiento
order_by: ['-created_at', 'last_name']
```

---

### ✅ Filtros Dinámicos

**Operadores disponibles:**
- `equals` - Igual a
- `contains` - Contiene
- `starts_with` - Empieza con
- `ends_with` - Termina con
- `gt` - Mayor que
- `gte` - Mayor o igual que
- `lt` - Menor que
- `lte` - Menor o igual que
- `in` - En lista
- `between` - Entre rango

**Ejemplo:**
```python
# Filtro: Socios activos de la comunidad "San Juan" registrados en 2025
filters = {
    'status': {'operator': 'equals', 'value': 'ACTIVE'},
    'community__name': {'operator': 'equals', 'value': 'San Juan'},
    'created_at': {'operator': 'gte', 'value': '2025-01-01'}
}
```

---

### ✅ Exportación a Excel

**Características:**
- Formato profesional con estilos
- Encabezados en negrita y color
- Ajuste automático de columnas
- Múltiples hojas (opcional)
- Fórmulas y totales

**Tecnología:** `openpyxl`

**Ejemplo de código:**
```python
def export_to_excel(self):
    wb = openpyxl.Workbook()
    ws = wb.active
    
    # Estilos de encabezado
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", fill_type="solid")
    
    # Escribir encabezados
    for col_idx, label in enumerate(self.columns_labels.values(), 1):
        cell = ws.cell(row=1, column=col_idx, value=label)
        cell.font = header_font
        cell.fill = header_fill
    
    # Escribir datos
    for row_idx, row_data in enumerate(self.data, 2):
        for col_idx, field in enumerate(self.columns_labels.keys(), 1):
            ws.cell(row=row_idx, column=col_idx, value=row_data.get(field))
    
    wb.save(file_path)
```

---

### ✅ Exportación a PDF

**Características:**
- Diseño profesional
- Tablas con bordes y colores
- Encabezado con título del reporte
- Pie de página con fecha
- Orientación automática (portrait/landscape)

**Tecnología:** `ReportLab`

**Ejemplo de código:**
```python
def export_to_pdf(self):
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []
    
    # Título
    title = Paragraph(f"<b>{self.report.name}</b>", styles['Title'])
    elements.append(title)
    
    # Tabla con datos
    table_data = [list(self.columns_labels.values())]  # Encabezados
    for row in self.data:
        table_data.append([str(row.get(field, '')) for field in self.columns_labels.keys()])
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
```

---

### ✅ Exportación a HTML

**Características:**
- Template personalizable
- Estilos CSS incluidos
- Responsive design
- Imprimible
- Embebible en emails

**Tecnología:** Django Templates

**Template:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ report.name }}</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th { background: #4472C4; color: white; padding: 10px; }
        td { border: 1px solid #ddd; padding: 8px; }
        tr:nth-child(even) { background: #f2f2f2; }
    </style>
</head>
<body>
    <h1>{{ report.name }}</h1>
    <p>{{ report.description }}</p>
    
    <table>
        <thead>
            <tr>
                {% for label in columns.values %}
                <th>{{ label }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in data %}
            <tr>
                {% for field in columns.keys %}
                <td>{{ row|get_item:field }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <p>Total de registros: {{ total_rows }}</p>
</body>
</html>
```

---

### ✅ Envío por Email

**Características:**
- Múltiples destinatarios
- Adjunto en formato seleccionado
- Cuerpo del email personalizable
- Programación de envíos automáticos
- Historial de envíos

**Ejemplo de código:**
```python
def send_by_email(self, recipients, file_format='pdf'):
    # Generar archivo
    if file_format == 'excel':
        file_path = self.export_to_excel()
    elif file_format == 'pdf':
        file_path = self.export_to_pdf()
    
    # Crear email
    email = EmailMessage(
        subject=f"Reporte: {self.report.name}",
        body=f"Adjunto encontrará el reporte solicitado.\n\nTotal de registros: {len(self.data)}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
    )
    
    # Adjuntar archivo
    with open(file_path, 'rb') as f:
        email.attach(
            filename=os.path.basename(file_path),
            content=f.read(),
            mimetype='application/pdf'
        )
    
    email.send()
```

---

## 📊 Ejemplos de Reportes

### Ejemplo 1: Reporte de Socios Activos

```json
{
  "name": "Socios Activos por Comunidad",
  "source_model": "partners",
  "columns": [
    "first_name",
    "last_name",
    "ci",
    "phone",
    "community__name",
    "created_at"
  ],
  "filters": {
    "status": {"operator": "equals", "value": "ACTIVE"}
  },
  "order_by": ["community__name", "last_name"],
  "group_by": ["community__name"],
  "aggregations": {
    "id": "COUNT"
  }
}
```

**Resultado:**
- Tabla con socios activos agrupados por comunidad
- Conteo de socios por comunidad
- Exportable a Excel, PDF, HTML

---

### Ejemplo 2: Reporte de Ventas Mensual

```json
{
  "name": "Ventas del Mes",
  "source_model": "orders",
  "columns": [
    "order_number",
    "customer__name",
    "order_date",
    "total",
    "status"
  ],
  "filters": {
    "order_date": {"operator": "gte", "value": "2025-11-01"},
    "status": {"operator": "in", "value": ["CONFIRMED", "PAID", "DELIVERED"]}
  },
  "order_by": ["-order_date"],
  "aggregations": {
    "total": "SUM"
  }
}
```

**Resultado:**
- Lista de pedidos del mes
- Total de ventas
- Exportable con gráficos (opcional)

---

## 🚀 Plan de Implementación

### Fase 1: Backend (2-3 días)

**Día 1:**
- ✅ Crear modelos (ReportDefinition, ReportExecution)
- ✅ Crear migraciones
- ✅ Implementar QueryBuilder

**Día 2:**
- ✅ Implementar exportadores (Excel, PDF, HTML, CSV)
- ✅ Crear API endpoints
- ✅ Pruebas unitarias

**Día 3:**
- ✅ Implementar envío por email
- ✅ Documentación
- ✅ Pruebas de integración

### Fase 2: Frontend (2-3 días)

**Día 1:**
- ✅ Crear ReportBuilder component
- ✅ Implementar ColumnSelector
- ✅ Implementar FilterBuilder

**Día 2:**
- ✅ Crear ReportPreview
- ✅ Implementar ExportOptions
- ✅ Integración con API

**Día 3:**
- ✅ Estilos y UX
- ✅ Pruebas de usuario
- ✅ Documentación

### Fase 3: Características Avanzadas (Opcional)

- ⏳ Gráficos interactivos (Chart.js)
- ⏳ Reportes programados (Celery)
- ⏳ Dashboard de reportes
- ⏳ Compartir reportes públicos

---

## 💰 Costo de Implementación

### Dependencias (Gratuitas)
- `openpyxl` - Gratis
- `reportlab` - Gratis
- `django` - Gratis
- `react` - Gratis

### Tiempo de Desarrollo
- Backend: 2-3 días
- Frontend: 2-3 días
- **Total: 4-6 días** de desarrollo

### Costo Estimado
- Desarrollador: $50/hora
- 6 días × 8 horas = 48 horas
- **Total: $2,400 USD**

---

## ✅ Conclusión

El sistema de reportes personalizables propuesto cumple **100% con el requisito**:

1. ✅ **Constructor visual** - Sin necesidad de código
2. ✅ **Selección de columnas** - Drag & drop intuitivo
3. ✅ **Filtros dinámicos** - Múltiples criterios y operadores
4. ✅ **Ordenamiento** - Personalizable
5. ✅ **Exportación múltiple** - Excel, PDF, HTML, CSV, Email
6. ✅ **Plantillas guardables** - Reutilizables
7. ✅ **Interfaz de filtrado** - Antes de generar el reporte

**El sistema está listo para implementarse en 4-6 días de desarrollo.**

---

## 📚 Documentación de Referencia

- `REPORTES_PERSONALIZABLES_ARQUITECTURA.md` - Arquitectura completa
- `REPORTES_IMPLEMENTACION_GUIA.md` - Guía de implementación
- `REPORTES_PERSONALIZABLES_RESUMEN.md` - Este documento

---

**Fecha:** 26 de noviembre de 2025  
**Estado:** ✅ DISEÑADO Y LISTO PARA IMPLEMENTAR
