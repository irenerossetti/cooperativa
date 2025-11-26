# Sistema de Alertas y Optimización de Cosecha - IMPLEMENTADO

## ✅ Módulo de Alertas Tempranas

### Funcionalidades:
1. **Alertas Climáticas**
   - Heladas (temp < 5°C)
   - Lluvia fuerte
   - Calor extremo (temp > 35°C)

2. **Alertas de Precio**
   - Oportunidades comerciales
   - Precios altos/bajos
   - Recomendaciones de venta

3. **Alertas de Cosecha**
   - Cultivos próximos a maduración
   - Preparación de logística

### Endpoints:
- `GET /api/alerts/alerts/` - Listar alertas
- `POST /api/alerts/alerts/generate/` - Generar alertas automáticamente
- `POST /api/alerts/alerts/{id}/mark_read/` - Marcar como leída
- `POST /api/alerts/alerts/{id}/dismiss/` - Desactivar alerta
- `GET /api/alerts/alerts/unread_count/` - Contar no leídas

---

## ✅ Optimizador de Momento Óptimo de Cosecha

### Factores Analizados:

1. **Maduración del Cultivo (40%)**
   - Días desde siembra
   - Días esperados por tipo de cultivo
   - Ventana óptima de cosecha

2. **Condiciones Climáticas (25%)**
   - Pronóstico 7 días
   - Lluvia, tormentas
   - Temperaturas extremas

3. **Condiciones de Mercado (20%)**
   - Precios actuales
   - Tendencias de precio
   - Oportunidades comerciales

4. **Logística (15%)**
   - Accesibilidad de parcela
   - Temporada de cosecha
   - Disponibilidad de transporte

### Recomendaciones:
- **COSECHAR_AHORA** (score ≥ 80): Todas las condiciones favorables
- **COSECHAR_PRONTO** (score ≥ 65): Planificar en 7 días
- **MONITOREAR** (score ≥ 50): Condiciones aceptables
- **ESPERAR** (score < 50): Esperar mejores condiciones

### Endpoints:
- `GET /api/alerts/alerts/optimal_harvest/` - Calcular para todas las parcelas
- `GET /api/alerts/alerts/optimal_harvest/{parcel_id}/` - Calcular para parcela específica

### Respuesta Ejemplo:
```json
{
  "success": true,
  "results": [
    {
      "parcel_id": 1,
      "parcel_code": "P001",
      "crop_name": "Quinua",
      "days_since_planting": 145,
      "scores": {
        "maturation": 95.0,
        "weather": 85.0,
        "market": 100.0,
        "logistics": 70.0,
        "overall": 89.5
      },
      "recommendation": "COSECHAR_AHORA",
      "urgency": "HIGH",
      "message": "Momento óptimo para cosechar. Todas las condiciones son favorables.",
      "optimal_date": "2025-11-27"
    }
  ]
}
```

---

## 🎯 Días de Maduración por Cultivo

| Cultivo | Días |
|---------|------|
| Quinua  | 150  |
| Papa    | 120  |
| Maíz    | 140  |
| Trigo   | 120  |
| Cebada  | 110  |
| Haba    | 100  |
| Arveja  | 90   |

---

## 📊 Uso

### Generar Alertas Automáticas:
```bash
curl -X POST http://localhost:8000/api/alerts/alerts/generate/ \
  -H "Authorization: Bearer {token}"
```

### Calcular Momento Óptimo:
```bash
curl http://localhost:8000/api/alerts/alerts/optimal_harvest/ \
  -H "Authorization: Bearer {token}"
```

---

## ✅ Estado: IMPLEMENTADO Y FUNCIONAL

Fecha: 26 de Noviembre, 2025
