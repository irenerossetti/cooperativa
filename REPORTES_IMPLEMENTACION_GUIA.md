# 📊 Sistema de Reportes Personalizables - Guía de Implementación

## 🚀 Instalación de Dependencias

### Backend (Python)

```bash
cd Backend
pip install openpyxl reportlab django-cors-headers
```

**Dependencias:**
- `openpyxl` - Generación de archivos Excel
- `reportlab` - Generación de archivos PDF
- `django-cors-headers` - CORS para el frontend

### Frontend (React)

```bash
cd Frontend
npm install react-grid-layout react-select react-datepicker file-saver
```

**Dependencias:**
- `react-grid-layout` - Drag & drop para constructor visual
- `react-select` - Selectores avanzados
- `react-datepicker` - Selector de fechas
- `file-saver` - Descarga de archivos

---

## 📁 Estructura de Archivos

```
Backend/
├── reports/
│   ├── __init__.py
│   ├── models.py              # Modelos de reportes
│   ├── serializers.py         # Serializers
│   ├── views.py               # API endpoints
│   ├── query_builder.py       # Constructor de queries
│   ├── exporters.py           # Exportadores (Excel, PDF, etc.)
│   ├── urls.py                # Rutas
│   ├── admin.py               # Admin de Django
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── templates/
│       └── reports/
│           └── report_template.html  # Template HTML

Frontend/
├── src/
│   ├── pages/
│   │   ├── ReportBuilder.jsx      # Constructor visual
│   │   ├── ReportsList.jsx        # Lista de reportes
│   │   └── ReportViewer.jsx       # Visualizador
│   ├── components/
│   │   ├── reports/
│   │   │   ├── ColumnSelector.jsx
│   │   │   ├── FilterBuilder.jsx
│   │   │   ├── ExportOptions.jsx
│   │   │   └── ReportPreview.jsx
│   └── services/
│       └── reportService.js       # API calls
```

---

## 🎨 Frontend - Constructor Visual de Reportes

### 1. Página Principal del Constructor

**Archivo:** `Frontend/src/pages/ReportBuilder.jsx`

```jsx
import React, { useState, useEffect } from 'react';
import { Save, Play, Download, Mail, Settings } from 'lucide-react';
import ColumnSelector from '../components/reports/ColumnSelector';
import FilterBuilder from '../components/reports/FilterBuilder';
import ReportPreview from '../components/reports/ReportPreview';
import ExportOptions from '../components/reports/ExportOptions';
import api from '../services/api';

const ReportBuilder = () => {
  const [reportConfig, setReportConfig] = useState({
    name: '',
    description: '',
    source_model: 'partners',
    columns: [],
    filters: {},
    order_by: [],
    group_by: [],
    aggregations: {},
  });
  
  const [availableColumns, setAvailableColumns] = useState({});
  const [reportData, setReportData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);

  // Modelos disponibles
  const sourceModels = [
    { value: 'partners', label: 'Socios' },
    { value: 'parcels', label: 'Parcelas' },
    { value: 'orders', label: 'Pedidos' },
    { value: 'products', label: 'Productos Cosechados' },
    { value: 'payments', label: 'Pagos' },
    { value: 'farm_activities', label: 'Labores Agrícolas' },
  ];

  useEffect(() => {
    if (reportConfig.source_model) {
      fetchAvailableColumns();
    }
  }, [reportConfig.source_model]);

  const fetchAvailableColumns = async () => {
    try {
      const response = await api.get(`/api/reports/models/${reportConfig.source_model}/columns/`);
      setAvailableColumns(response.data.columns);
    } catch (error) {
      console.error('Error fetching columns:', error);
    }
  };

  const handleExecuteReport = async () => {
    setLoading(true);
    try {
      const response = await api.post('/api/reports/execute/', reportConfig);
      setReportData(response.data.data);
    } catch (error) {
      console.error('Error executing report:', error);
      alert('Error al ejecutar el reporte');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveReport = async () => {
    try {
      await api.post('/api/reports/definitions/', reportConfig);
      alert('Reporte guardado exitosamente');
    } catch (error) {
      console.error('Error saving report:', error);
      alert('Error al guardar el reporte');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">Constructor de Reportes</h1>
            <p className="text-emerald-200/80">Crea reportes personalizados con filtros y exportación</p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleSaveReport}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
            >
              <Save className="w-4 h-4" />
              <span>Guardar</span>
            </button>
            <button
              onClick={handleExecuteReport}
              disabled={loading}
              className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 disabled:opacity-50"
            >
              <Play className="w-4 h-4" />
              <span>{loading ? 'Ejecutando...' : 'Ejecutar'}</span>
            </button>
            <button
              onClick={() => setShowExportModal(true)}
              disabled={reportData.length === 0}
              className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 disabled:opacity-50"
            >
              <Download className="w-4 h-4" />
              <span>Exportar</span>
            </button>
          </div>
        </div>
      </div>

      {/* Configuración del Reporte */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Panel Izquierdo - Configuración */}
        <div className="lg:col-span-1 space-y-6">
          {/* Información Básica */}
          <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Información Básica</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-white/90 text-sm font-medium mb-2">
                  Nombre del Reporte *
                </label>
                <input
                  type="text"
                  value={reportConfig.name}
                  onChange={(e) => setReportConfig({...reportConfig, name: e.target.value})}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
                  placeholder="Ej: Reporte de Ventas Mensual"
                />
              </div>

              <div>
                <label className="block text-white/90 text-sm font-medium mb-2">
                  Descripción
                </label>
                <textarea
                  value={reportConfig.description}
                  onChange={(e) => setReportConfig({...reportConfig, description: e.target.value})}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
                  rows="3"
                  placeholder="Descripción del reporte..."
                />
              </div>

              <div>
                <label className="block text-white/90 text-sm font-medium mb-2">
                  Fuente de Datos *
                </label>
                <select
                  value={reportConfig.source_model}
                  onChange={(e) => setReportConfig({
                    ...reportConfig, 
                    source_model: e.target.value,
                    columns: [],
                    filters: {}
                  })}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
                >
                  {sourceModels.map(model => (
                    <option key={model.value} value={model.value}>
                      {model.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Selector de Columnas */}
          <ColumnSelector
            availableColumns={availableColumns}
            selectedColumns={reportConfig.columns}
            onChange={(columns) => setReportConfig({...reportConfig, columns})}
          />

          {/* Constructor de Filtros */}
          <FilterBuilder
            availableColumns={availableColumns}
            filters={reportConfig.filters}
            onChange={(filters) => setReportConfig({...reportConfig, filters})}
          />
        </div>

        {/* Panel Derecho - Vista Previa */}
        <div className="lg:col-span-2">
          <ReportPreview
            data={reportData}
            columns={reportConfig.columns}
            columnLabels={availableColumns}
            loading={loading}
          />
        </div>
      </div>

      {/* Modal de Exportación */}
      {showExportModal && (
        <ExportOptions
          reportConfig={reportConfig}
          reportData={reportData}
          onClose={() => setShowExportModal(false)}
        />
      )}
    </div>
  );
};

export default ReportBuilder;
```

---

### 2. Selector de Columnas

**Archivo:** `Frontend/src/components/reports/ColumnSelector.jsx`

```jsx
import React from 'react';
import { Plus, X, GripVertical } from 'lucide-react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const ColumnSelector = ({ availableColumns, selectedColumns, onChange }) => {
  const [showAddColumn, setShowAddColumn] = useState(false);

  const handleAddColumn = (columnKey) => {
    if (!selectedColumns.includes(columnKey)) {
      onChange([...selectedColumns, columnKey]);
    }
    setShowAddColumn(false);
  };

  const handleRemoveColumn = (columnKey) => {
    onChange(selectedColumns.filter(col => col !== columnKey));
  };

  const handleDragEnd = (result) => {
    if (!result.destination) return;

    const items = Array.from(selectedColumns);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    onChange(items);
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-white">Columnas</h3>
        <button
          onClick={() => setShowAddColumn(!showAddColumn)}
          className="bg-emerald-500 hover:bg-emerald-600 text-white p-2 rounded-lg"
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>

      {/* Lista de columnas seleccionadas */}
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="columns">
          {(provided) => (
            <div
              {...provided.droppableProps}
              ref={provided.innerRef}
              className="space-y-2"
            >
              {selectedColumns.map((columnKey, index) => (
                <Draggable key={columnKey} draggableId={columnKey} index={index}>
                  {(provided) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      className="bg-white/5 border border-white/10 rounded-lg p-3 flex items-center justify-between"
                    >
                      <div className="flex items-center space-x-2">
                        <div {...provided.dragHandleProps}>
                          <GripVertical className="w-4 h-4 text-white/60" />
                        </div>
                        <span className="text-white text-sm">
                          {availableColumns[columnKey] || columnKey}
                        </span>
                      </div>
                      <button
                        onClick={() => handleRemoveColumn(columnKey)}
                        className="text-red-400 hover:text-red-300"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>

      {/* Selector de nueva columna */}
      {showAddColumn && (
        <div className="mt-4 bg-white/5 border border-white/10 rounded-lg p-4">
          <p className="text-white/80 text-sm mb-2">Selecciona una columna:</p>
          <div className="space-y-1 max-h-60 overflow-y-auto">
            {Object.entries(availableColumns).map(([key, label]) => (
              <button
                key={key}
                onClick={() => handleAddColumn(key)}
                disabled={selectedColumns.includes(key)}
                className="w-full text-left px-3 py-2 text-white text-sm hover:bg-white/10 rounded disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {label}
              </button>
            ))}
          </div>
        </div>
      )}

      {selectedColumns.length === 0 && (
        <p className="text-white/60 text-sm text-center py-4">
          No hay columnas seleccionadas. Haz clic en + para agregar.
        </p>
      )}
    </div>
  );
};

export default ColumnSelector;
```

---

### 3. Constructor de Filtros

**Archivo:** `Frontend/src/components/reports/FilterBuilder.jsx`

```jsx
import React, { useState } from 'react';
import { Plus, X, Filter } from 'lucide-react';

const FilterBuilder = ({ availableColumns, filters, onChange }) => {
  const [showAddFilter, setShowAddFilter] = useState(false);

  const operators = [
    { value: 'equals', label: 'Igual a' },
    { value: 'contains', label: 'Contiene' },
    { value: 'starts_with', label: 'Empieza con' },
    { value: 'ends_with', label: 'Termina con' },
    { value: 'gt', label: 'Mayor que' },
    { value: 'gte', label: 'Mayor o igual que' },
    { value: 'lt', label: 'Menor que' },
    { value: 'lte', label: 'Menor o igual que' },
  ];

  const handleAddFilter = (field) => {
    onChange({
      ...filters,
      [field]: { operator: 'equals', value: '' }
    });
    setShowAddFilter(false);
  };

  const handleUpdateFilter = (field, key, value) => {
    onChange({
      ...filters,
      [field]: { ...filters[field], [key]: value }
    });
  };

  const handleRemoveFilter = (field) => {
    const newFilters = { ...filters };
    delete newFilters[field];
    onChange(newFilters);
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
          <Filter className="w-5 h-5" />
          <span>Filtros</span>
        </h3>
        <button
          onClick={() => setShowAddFilter(!showAddFilter)}
          className="bg-emerald-500 hover:bg-emerald-600 text-white p-2 rounded-lg"
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>

      {/* Filtros activos */}
      <div className="space-y-3">
        {Object.entries(filters).map(([field, config]) => (
          <div key={field} className="bg-white/5 border border-white/10 rounded-lg p-3">
            <div className="flex justify-between items-start mb-2">
              <span className="text-white text-sm font-medium">
                {availableColumns[field] || field}
              </span>
              <button
                onClick={() => handleRemoveFilter(field)}
                className="text-red-400 hover:text-red-300"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <select
                value={config.operator}
                onChange={(e) => handleUpdateFilter(field, 'operator', e.target.value)}
                className="bg-white/10 border border-white/20 rounded px-2 py-1 text-white text-sm"
              >
                {operators.map(op => (
                  <option key={op.value} value={op.value}>{op.label}</option>
                ))}
              </select>

              <input
                type="text"
                value={config.value}
                onChange={(e) => handleUpdateFilter(field, 'value', e.target.value)}
                className="bg-white/10 border border-white/20 rounded px-2 py-1 text-white text-sm"
                placeholder="Valor..."
              />
            </div>
          </div>
        ))}
      </div>

      {/* Selector de nuevo filtro */}
      {showAddFilter && (
        <div className="mt-4 bg-white/5 border border-white/10 rounded-lg p-4">
          <p className="text-white/80 text-sm mb-2">Selecciona un campo:</p>
          <div className="space-y-1 max-h-40 overflow-y-auto">
            {Object.entries(availableColumns).map(([key, label]) => (
              <button
                key={key}
                onClick={() => handleAddFilter(key)}
                disabled={filters[key]}
                className="w-full text-left px-3 py-2 text-white text-sm hover:bg-white/10 rounded disabled:opacity-50"
              >
                {label}
              </button>
            ))}
          </div>
        </div>
      )}

      {Object.keys(filters).length === 0 && (
        <p className="text-white/60 text-sm text-center py-4">
          No hay filtros aplicados. Haz clic en + para agregar.
        </p>
      )}
    </div>
  );
};

export default FilterBuilder;
```

---

## 📝 Continuará...

¿Quieres que continúe con:
1. Componente de Vista Previa
2. Modal de Exportación
3. Ejemplos de uso completos
4. Instalación paso a paso

?
