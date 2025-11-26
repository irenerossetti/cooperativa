from datetime import datetime, timedelta
from django.utils import timezone
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
                
                alerts.append({
                    'type': 'PRICE',
                    'severity': severity,
                    'title': f"{alert['product']} - {alert['message']}",
                    'message': alert['recommendation'],
                    'data': {'product': alert['product'], 'variation': alert['variation']}
                })
        
        except Exception as e:
            print(f"Error checking price alerts: {e}")
        
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
        all_alerts.extend(self.check_weather_alerts())
        all_alerts.extend(self.check_price_alerts())
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
