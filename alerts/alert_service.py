from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from .models import Alert
from weather.weather_service import WeatherService
from market_analysis.market_service import MarketAnalysisService


class AlertService:
    """Servicio para generar alertas automáticas"""
    
    def __init__(self, organization):
        self.organization = organization
    
    def check_weather_alerts(self, lat=-17.78, lon=-63.18):
        """Verifica condiciones climáticas adversas"""
        alerts = []
        
        try:
            weather_service = WeatherService()
            forecast = weather_service.get_forecast(lat, lon)
            
            if not forecast or 'list' not in forecast:
                return alerts
            
            # Revisar próximos 3 días
            for day in forecast['list'][:3]:
                weather_main = day['weather'][0]['main'].lower()
                temp = day['main']['temp']
                
                # Alerta por lluvia fuerte
                if 'rain' in weather_main or 'thunderstorm' in weather_main:
                    alerts.append({
                        'type': 'WEATHER',
                        'severity': 'HIGH',
                        'title': 'Lluvia Fuerte Próxima',
                        'message': f'Se pronostica lluvia fuerte. Considere posponer labores de campo.',
                        'data': {'weather': weather_main, 'temp': temp}
                    })
                
                # Alerta por helada
                if temp < 5:
                    alerts.append({
                        'type': 'WEATHER',
                        'severity': 'CRITICAL',
                        'title': 'Riesgo de Helada',
                        'message': f'Temperatura muy baja ({temp}°C). Proteja cultivos sensibles.',
                        'data': {'temp': temp}
                    })
                
                # Alerta por calor extremo
                if temp > 35:
                    alerts.append({
                        'type': 'WEATHER',
                        'severity': 'MEDIUM',
                        'title': 'Calor Extremo',
                        'message': f'Temperatura alta ({temp}°C). Asegure riego adecuado.',
                        'data': {'temp': temp}
                    })
        
        except Exception as e:
            print(f"Error checking weather alerts: {e}")
        
        return alerts
    
    def check_price_alerts(self):
        """Verifica oportunidades de precio"""
        alerts = []
        
        try:
            market_service = MarketAnalysisService(self.organization)
            price_alerts = market_service.get_price_alerts()
            
            for alert in price_alerts:
                severity = 'HIGH' if alert['priority'] == 'high' else 'MEDIUM'
                
                # Mensaje más específico con detalles de precio
                product_name = alert['product']
                variation = alert['variation']
                
                # Crear mensaje detallado
                if variation > 0:
                    price_trend = f"subió +{variation:.1f}%"
                    emoji = "📈"
                else:
                    price_trend = f"bajó {variation:.1f}%"
                    emoji = "📉"
                
                detailed_message = f"{emoji} El precio de {product_name} {price_trend}. {alert['recommendation']}"
                
                alerts.append({
                    'type': 'PRICE',
                    'severity': severity,
                    'title': f"{product_name} - {alert['message']}",
                    'message': detailed_message,
                    'data': {
                        'product': product_name, 
                        'variation': variation,
                        'trend': 'up' if variation > 0 else 'down'
                    }
                })
        
        except Exception as e:
            print(f"Error checking price alerts: {e}")
        
        return alerts
    
    def check_stock_alerts(self):
        """Verifica productos con stock bajo"""
        alerts = []
        
        try:
            from inventory.models import InventoryItem
            
            # Obtener items con stock bajo
            low_stock_items = InventoryItem.objects.filter(
                organization=self.organization,
                current_stock__lte=models.F('minimum_stock'),
                current_stock__gt=0
            )
            
            # Agrupar por severidad
            critical_items = []
            warning_items = []
            
            for item in low_stock_items:
                stock_percentage = (item.current_stock / item.minimum_stock * 100) if item.minimum_stock > 0 else 0
                
                if stock_percentage <= 25:  # Stock crítico (25% o menos del mínimo)
                    critical_items.append(item)
                else:
                    warning_items.append(item)
            
            # Crear alerta para items críticos
            if critical_items:
                if len(critical_items) == 1:
                    item = critical_items[0]
                    message = f"🔴 Stock crítico: {item.name} solo tiene {float(item.current_stock)} {item.unit_of_measure} disponibles (mínimo: {float(item.minimum_stock)})"
                else:
                    products_list = ", ".join([f"{item.name} ({float(item.current_stock)} {item.unit_of_measure})" for item in critical_items[:3]])
                    if len(critical_items) > 3:
                        products_list += f" y {len(critical_items) - 3} más"
                    message = f"🔴 {len(critical_items)} productos en stock crítico: {products_list}. Reabastezca urgentemente."
                
                alerts.append({
                    'type': 'STOCK',
                    'severity': 'CRITICAL',
                    'title': 'Stock Crítico',
                    'message': message,
                    'data': {
                        'items': [{'id': item.id, 'name': item.name, 'stock': float(item.current_stock), 'min': float(item.minimum_stock)} for item in critical_items]
                    }
                })
            
            # Crear alerta para items con advertencia
            if warning_items:
                if len(warning_items) == 1:
                    item = warning_items[0]
                    message = f"⚠️ Stock bajo: {item.name} tiene {float(item.current_stock)} {item.unit_of_measure} (mínimo: {float(item.minimum_stock)}). Considere reabastecer pronto."
                else:
                    products_list = ", ".join([f"{item.name} ({float(item.current_stock)} {item.unit_of_measure})" for item in warning_items[:3]])
                    if len(warning_items) > 3:
                        products_list += f" y {len(warning_items) - 3} más"
                    message = f"⚠️ {len(warning_items)} productos con stock bajo: {products_list}. Planifique reabastecimiento."
                
                alerts.append({
                    'type': 'STOCK',
                    'severity': 'MEDIUM',
                    'title': 'Stock Bajo',
                    'message': message,
                    'data': {
                        'items': [{'id': item.id, 'name': item.name, 'stock': float(item.current_stock), 'min': float(item.minimum_stock)} for item in warning_items]
                    }
                })
        
        except Exception as e:
            print(f"Error checking stock alerts: {e}")
        
        return alerts
    
    def check_harvest_alerts(self):
        """Verifica cultivos próximos a cosecha"""
        alerts = []
        
        try:
            from parcels.models import Parcel
            from datetime import date
            
            # Obtener parcelas con cultivos activos
            parcels = Parcel.objects.filter(
                organization=self.organization,
                current_crop__isnull=False
            )
            
            for parcel in parcels:
                # Estimar tiempo de cosecha (simplificado - 120 días desde siembra)
                if parcel.planting_date:
                    days_since_planting = (date.today() - parcel.planting_date).days
                    
                    # Alerta si está cerca de cosecha (100-120 días)
                    if 100 <= days_since_planting <= 120:
                        alerts.append({
                            'type': 'HARVEST',
                            'severity': 'MEDIUM',
                            'title': f'Parcela {parcel.code} Próxima a Cosecha',
                            'message': f'El cultivo de {parcel.current_crop.name} tiene {days_since_planting} días. Prepare logística de cosecha.',
                            'data': {'parcel_id': parcel.id, 'days': days_since_planting}
                        })
        
        except Exception as e:
            print(f"Error checking harvest alerts: {e}")
        
        return alerts
    
    def generate_all_alerts(self):
        """Genera todas las alertas y las guarda en BD"""
        all_alerts = []
        
        # Recopilar alertas
        all_alerts.extend(self.check_stock_alerts())  # Primero stock (más importante)
        all_alerts.extend(self.check_price_alerts())
        all_alerts.extend(self.check_weather_alerts())
        all_alerts.extend(self.check_harvest_alerts())
        
        # Guardar en BD (evitar duplicados)
        created_alerts = []
        for alert_data in all_alerts:
            # Verificar si ya existe una alerta similar activa
            existing = Alert.objects.filter(
                organization=self.organization,
                alert_type=alert_data['type'],
                title=alert_data['title'],
                is_active=True,
                created_at__gte=timezone.now() - timedelta(hours=24)
            ).exists()
            
            if not existing:
                alert = Alert.objects.create(
                    organization=self.organization,
                    alert_type=alert_data['type'],
                    severity=alert_data['severity'],
                    title=alert_data['title'],
                    message=alert_data['message'],
                    data=alert_data.get('data', {}),
                    expires_at=timezone.now() + timedelta(days=7)
                )
                created_alerts.append(alert)
        
        return created_alerts
