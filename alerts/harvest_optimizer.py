from datetime import datetime, timedelta, date
from weather.weather_service import WeatherService
from market_analysis.market_service import MarketAnalysisService


class HarvestOptimizer:
    """Servicio para calcular el momento óptimo de cosecha"""
    
    # Días de maduración por cultivo (simplificado)
    MATURATION_DAYS = {
        'QUINUA': 150,
        'PAPA': 120,
        'MAIZ': 140,
        'TRIGO': 120,
        'CEBADA': 110,
        'HABA': 100,
        'ARVEJA': 90,
    }
    
    def __init__(self, organization):
        self.organization = organization
        self.weather_service = WeatherService()
        self.market_service = MarketAnalysisService(organization)
    
    def get_planting_date(self, parcel):
        """Obtiene la fecha de siembra de la parcela desde farm_activities"""
        from farm_activities.models import FarmActivity
        
        # Buscar la actividad de siembra más reciente para esta parcela
        planting_activity = FarmActivity.objects.filter(
            parcel=parcel,
            activity_type='SIEMBRA'
        ).order_by('-activity_date').first()
        
        if planting_activity:
            return planting_activity.activity_date
        
        # Si no hay actividad de siembra, usar fecha de creación de la parcela como aproximación
        return parcel.created_at.date() if hasattr(parcel.created_at, 'date') else parcel.created_at
    
    def calculate_maturation_score(self, parcel):
        """Calcula score de maduración (0-100)"""
        if not parcel.current_crop:
            return 0
        
        planting_date = self.get_planting_date(parcel)
        if not planting_date:
            return 0
        
        crop_name = parcel.current_crop.name.upper()
        expected_days = self.MATURATION_DAYS.get(crop_name, 120)
        
        days_since_planting = (date.today() - planting_date).days
        
        # Score basado en proximidad a días esperados
        if days_since_planting < expected_days * 0.8:
            # Muy temprano
            score = (days_since_planting / (expected_days * 0.8)) * 50
        elif days_since_planting <= expected_days * 1.1:
            # Ventana óptima
            score = 80 + ((days_since_planting - expected_days * 0.8) / (expected_days * 0.3)) * 20
        else:
            # Pasado de maduración
            score = max(0, 100 - (days_since_planting - expected_days * 1.1) * 2)
        
        return min(100, max(0, score))
    
    def calculate_weather_score(self, lat=-17.78, lon=-63.18):
        """Calcula score de condiciones climáticas (0-100)"""
        try:
            forecast = self.weather_service.get_forecast(lat, lon)
            
            if not forecast or 'list' not in forecast:
                return 50  # Score neutral si no hay datos
            
            score = 100
            
            # Revisar próximos 7 días
            for day in forecast['list'][:7]:
                weather_main = day['weather'][0]['main'].lower()
                
                # Penalizar lluvia
                if 'rain' in weather_main:
                    score -= 15
                elif 'thunderstorm' in weather_main:
                    score -= 25
                
                # Penalizar temperaturas extremas
                temp = day['main']['temp']
                if temp < 5 or temp > 35:
                    score -= 10
            
            return max(0, min(100, score))
        
        except Exception as e:
            print(f"Error calculating weather score: {e}")
            return 50
    
    def calculate_market_score(self, crop_name):
        """Calcula score de condiciones de mercado (0-100)"""
        try:
            trends = self.market_service.get_market_trends()
            
            # Buscar el cultivo en las tendencias
            for trend in trends:
                if crop_name.upper() in trend['product'].upper():
                    variation = trend['variation']
                    
                    # Score basado en variación de precio
                    if variation > 10:
                        return 100  # Precio muy alto, vender ahora
                    elif variation > 5:
                        return 80
                    elif variation > 0:
                        return 60
                    elif variation > -5:
                        return 40
                    else:
                        return 20  # Precio bajo, esperar si es posible
            
            return 50  # Score neutral si no hay datos
        
        except Exception as e:
            print(f"Error calculating market score: {e}")
            return 50
    
    def calculate_logistics_score(self, parcel):
        """Calcula score de logística (0-100)"""
        # Factores logísticos simplificados
        score = 70  # Base score
        
        # Penalizar si está muy lejos (simplificado)
        # En producción, calcularías distancia real a centros de acopio
        
        # Bonus si hay buena accesibilidad
        if hasattr(parcel, 'accessibility') and parcel.accessibility == 'GOOD':
            score += 20
        
        # Penalizar si es temporada alta (mucha demanda de transporte)
        current_month = date.today().month
        if current_month in [4, 5, 6]:  # Temporada alta de cosecha
            score -= 15
        
        return min(100, max(0, score))
    
    def calculate_optimal_harvest(self, parcel):
        """Calcula el momento óptimo de cosecha para una parcela"""
        
        if not parcel.current_crop:
            return {
                'parcel_id': parcel.id,
                'parcel_code': parcel.code,
                'status': 'NO_DATA',
                'message': 'Parcela sin cultivo activo',
                'overall_score': 0
            }
        
        planting_date = self.get_planting_date(parcel)
        if not planting_date:
            return {
                'parcel_id': parcel.id,
                'parcel_code': parcel.code,
                'status': 'NO_DATA',
                'message': 'No se encontró fecha de siembra',
                'overall_score': 0
            }
        
        # Calcular scores individuales
        maturation_score = self.calculate_maturation_score(parcel)
        weather_score = self.calculate_weather_score()
        market_score = self.calculate_market_score(parcel.current_crop.name)
        logistics_score = self.calculate_logistics_score(parcel)
        
        # Pesos para cada factor
        weights = {
            'maturation': 0.40,  # 40% - Lo más importante
            'weather': 0.25,     # 25%
            'market': 0.20,      # 20%
            'logistics': 0.15    # 15%
        }
        
        # Score general ponderado
        overall_score = (
            maturation_score * weights['maturation'] +
            weather_score * weights['weather'] +
            market_score * weights['market'] +
            logistics_score * weights['logistics']
        )
        
        # Determinar recomendación
        if overall_score >= 80:
            recommendation = 'COSECHAR_AHORA'
            message = 'Momento óptimo para cosechar. Todas las condiciones son favorables.'
            urgency = 'HIGH'
        elif overall_score >= 65:
            recommendation = 'COSECHAR_PRONTO'
            message = 'Condiciones buenas. Planifique cosecha en los próximos 7 días.'
            urgency = 'MEDIUM'
        elif overall_score >= 50:
            recommendation = 'MONITOREAR'
            message = 'Condiciones aceptables. Monitoree clima y precios.'
            urgency = 'LOW'
        else:
            recommendation = 'ESPERAR'
            message = 'Condiciones no óptimas. Espere mejores condiciones.'
            urgency = 'LOW'
        
        # Calcular fecha estimada óptima
        days_since_planting = (date.today() - planting_date).days
        crop_name = parcel.current_crop.name.upper()
        expected_days = self.MATURATION_DAYS.get(crop_name, 120)
        
        if days_since_planting < expected_days:
            days_to_optimal = expected_days - days_since_planting
            optimal_date = date.today() + timedelta(days=days_to_optimal)
        else:
            optimal_date = date.today()
        
        return {
            'parcel_id': parcel.id,
            'parcel_code': parcel.code,
            'crop_name': parcel.current_crop.name,
            'planting_date': planting_date.isoformat(),
            'days_since_planting': days_since_planting,
            'scores': {
                'maturation': round(maturation_score, 1),
                'weather': round(weather_score, 1),
                'market': round(market_score, 1),
                'logistics': round(logistics_score, 1),
                'overall': round(overall_score, 1)
            },
            'recommendation': recommendation,
            'urgency': urgency,
            'message': message,
            'optimal_date': optimal_date.isoformat(),
            'status': 'OK'
        }
    
    def calculate_all_parcels(self):
        """Calcula momento óptimo para todas las parcelas con cultivos activos"""
        from parcels.models import Parcel
        
        parcels = Parcel.objects.filter(
            organization=self.organization,
            current_crop__isnull=False
        )
        
        results = []
        for parcel in parcels:
            result = self.calculate_optimal_harvest(parcel)
            results.append(result)
        
        # Ordenar por score general (mayor a menor)
        results.sort(key=lambda x: x.get('scores', {}).get('overall', 0), reverse=True)
        
        return results
