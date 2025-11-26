"""
Servicio para obtener datos del clima usando OpenWeatherMap API
"""
import os
import urllib.request
import urllib.error
import json
from datetime import datetime, timedelta


class WeatherService:
    """Servicio para interactuar con OpenWeatherMap API"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            print("⚠️ OPENWEATHER_API_KEY no configurada - usando datos simulados")
    
    def get_current_weather(self, lat, lon):
        """
        Obtiene el clima actual para una ubicación
        
        Args:
            lat: Latitud
            lon: Longitud
        
        Returns:
            dict: Datos del clima actual
        """
        if not self.api_key:
            return self._get_simulated_current_weather(lat, lon)
        
        try:
            url = f"{self.BASE_URL}/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang=es"
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                return {
                    'temperature': round(data['main']['temp'], 1),
                    'feels_like': round(data['main']['feels_like'], 1),
                    'temp_min': round(data['main']['temp_min'], 1),
                    'temp_max': round(data['main']['temp_max'], 1),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # m/s a km/h
                    'wind_direction': data['wind'].get('deg', 0),
                    'clouds': data['clouds']['all'],
                    'description': data['weather'][0]['description'].capitalize(),
                    'icon': data['weather'][0]['icon'],
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                    'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                    'location': data['name'],
                    'country': data['sys']['country'],
                    'timestamp': datetime.now().isoformat()
                }
        
        except Exception as e:
            print(f"Error al obtener clima actual: {e}")
            return self._get_simulated_current_weather(lat, lon)
    
    def get_forecast(self, lat, lon, days=5):
        """
        Obtiene el pronóstico del clima para los próximos días
        
        Args:
            lat: Latitud
            lon: Longitud
            days: Número de días (máximo 5)
        
        Returns:
            list: Lista de pronósticos por día
        """
        if not self.api_key:
            return self._get_simulated_forecast(lat, lon, days)
        
        try:
            url = f"{self.BASE_URL}/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang=es"
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                # Agrupar por día
                daily_forecast = {}
                for item in data['list']:
                    date = datetime.fromtimestamp(item['dt']).date()
                    
                    if date not in daily_forecast:
                        daily_forecast[date] = {
                            'date': date.isoformat(),
                            'day_name': self._get_day_name(date),
                            'temp_min': item['main']['temp_min'],
                            'temp_max': item['main']['temp_max'],
                            'humidity': item['main']['humidity'],
                            'description': item['weather'][0]['description'].capitalize(),
                            'icon': item['weather'][0]['icon'],
                            'wind_speed': round(item['wind']['speed'] * 3.6, 1),
                            'rain_probability': item.get('pop', 0) * 100,
                            'clouds': item['clouds']['all']
                        }
                    else:
                        # Actualizar min/max
                        daily_forecast[date]['temp_min'] = min(
                            daily_forecast[date]['temp_min'],
                            item['main']['temp_min']
                        )
                        daily_forecast[date]['temp_max'] = max(
                            daily_forecast[date]['temp_max'],
                            item['main']['temp_max']
                        )
                
                # Convertir a lista y limitar días
                forecast_list = list(daily_forecast.values())[:days]
                
                # Redondear temperaturas
                for day in forecast_list:
                    day['temp_min'] = round(day['temp_min'], 1)
                    day['temp_max'] = round(day['temp_max'], 1)
                    day['rain_probability'] = round(day['rain_probability'])
                
                return forecast_list
        
        except Exception as e:
            print(f"Error al obtener pronóstico: {e}")
            return self._get_simulated_forecast(lat, lon, days)
    
    def get_agricultural_data(self, lat, lon):
        """
        Obtiene datos específicos para agricultura
        
        Args:
            lat: Latitud
            lon: Longitud
        
        Returns:
            dict: Datos agrícolas
        """
        current = self.get_current_weather(lat, lon)
        forecast = self.get_forecast(lat, lon, 3)
        
        # Calcular alertas agrícolas
        alerts = []
        recommendations = []
        
        # Alerta de lluvia
        if forecast and forecast[0]['rain_probability'] > 70:
            alerts.append({
                'type': 'rain',
                'severity': 'warning',
                'message': f"⚠️ Alta probabilidad de lluvia ({forecast[0]['rain_probability']}%) en las próximas 24h"
            })
            recommendations.append("Posponer aplicación de pesticidas y fertilizantes foliares")
        
        # Alerta de viento
        if current['wind_speed'] > 20:
            alerts.append({
                'type': 'wind',
                'severity': 'warning',
                'message': f"💨 Vientos fuertes ({current['wind_speed']} km/h)"
            })
            recommendations.append("No aplicar productos químicos - riesgo de deriva")
        
        # Alerta de temperatura
        if current['temperature'] > 35:
            alerts.append({
                'type': 'heat',
                'severity': 'danger',
                'message': f"🌡️ Temperatura muy alta ({current['temperature']}°C)"
            })
            recommendations.append("Aumentar frecuencia de riego - riesgo de estrés hídrico")
        elif current['temperature'] < 5:
            alerts.append({
                'type': 'frost',
                'severity': 'danger',
                'message': f"❄️ Riesgo de helada ({current['temperature']}°C)"
            })
            recommendations.append("Proteger cultivos sensibles - riesgo de daño por frío")
        
        # Condiciones ideales
        if (20 <= current['temperature'] <= 28 and 
            current['wind_speed'] < 15 and 
            forecast[0]['rain_probability'] < 30):
            recommendations.append("✅ Condiciones ideales para aplicación de productos")
            recommendations.append("✅ Buen momento para labores de campo")
        
        return {
            'current': current,
            'forecast': forecast,
            'alerts': alerts,
            'recommendations': recommendations,
            'agricultural_index': {
                'irrigation_need': self._calculate_irrigation_need(current, forecast),
                'spray_conditions': self._calculate_spray_conditions(current),
                'harvest_conditions': self._calculate_harvest_conditions(current, forecast)
            }
        }
    
    def _calculate_irrigation_need(self, current, forecast):
        """Calcula necesidad de riego (0-100)"""
        score = 0
        
        # Temperatura alta aumenta necesidad
        if current['temperature'] > 30:
            score += 30
        elif current['temperature'] > 25:
            score += 20
        
        # Humedad baja aumenta necesidad
        if current['humidity'] < 40:
            score += 30
        elif current['humidity'] < 60:
            score += 15
        
        # Sin lluvia próxima aumenta necesidad
        if forecast and forecast[0]['rain_probability'] < 20:
            score += 40
        
        return min(score, 100)
    
    def _calculate_spray_conditions(self, current):
        """Calcula condiciones para fumigación (0-100)"""
        score = 100
        
        # Viento reduce score
        if current['wind_speed'] > 15:
            score -= 50
        elif current['wind_speed'] > 10:
            score -= 25
        
        # Temperatura muy alta o baja reduce score
        if current['temperature'] > 30 or current['temperature'] < 10:
            score -= 30
        
        # Humedad muy baja reduce score
        if current['humidity'] < 50:
            score -= 20
        
        return max(score, 0)
    
    def _calculate_harvest_conditions(self, current, forecast):
        """Calcula condiciones para cosecha (0-100)"""
        score = 100
        
        # Lluvia próxima reduce score
        if forecast and forecast[0]['rain_probability'] > 50:
            score -= 60
        elif forecast and forecast[0]['rain_probability'] > 30:
            score -= 30
        
        # Humedad alta reduce score
        if current['humidity'] > 80:
            score -= 20
        
        return max(score, 0)
    
    def _get_day_name(self, date):
        """Obtiene el nombre del día en español"""
        days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return days[date.weekday()]
    
    def _get_simulated_current_weather(self, lat, lon):
        """Genera datos simulados de clima actual basados en ubicación real"""
        # Datos climáticos realistas por ciudad de Bolivia
        city_weather = {
            # Santa Cruz - Tropical, caluroso y húmedo
            (-17.78, -63.18): {
                'temp': 28, 'humidity': 70, 'wind': 15, 'clouds': 40,
                'desc': 'Parcialmente nublado', 'icon': '02d', 'location': 'Santa Cruz'
            },
            # La Paz - Frío de altura, seco
            (-16.50, -68.15): {
                'temp': 12, 'humidity': 45, 'wind': 20, 'clouds': 30,
                'desc': 'Despejado', 'icon': '01d', 'location': 'La Paz'
            },
            # Cochabamba - Templado, agradable
            (-17.39, -66.16): {
                'temp': 22, 'humidity': 50, 'wind': 10, 'clouds': 20,
                'desc': 'Soleado', 'icon': '01d', 'location': 'Cochabamba'
            },
            # Sucre - Templado de altura
            (-19.03, -65.26): {
                'temp': 18, 'humidity': 55, 'wind': 12, 'clouds': 35,
                'desc': 'Parcialmente nublado', 'icon': '02d', 'location': 'Sucre'
            },
            # Tarija - Templado, seco
            (-21.53, -64.73): {
                'temp': 24, 'humidity': 48, 'wind': 8, 'clouds': 15,
                'desc': 'Despejado', 'icon': '01d', 'location': 'Tarija'
            },
            # Potosí - Muy frío de altura
            (-19.58, -65.75): {
                'temp': 8, 'humidity': 40, 'wind': 25, 'clouds': 50,
                'desc': 'Nublado', 'icon': '03d', 'location': 'Potosí'
            },
            # Oruro - Frío de altura, ventoso
            (-17.98, -67.13): {
                'temp': 10, 'humidity': 42, 'wind': 22, 'clouds': 45,
                'desc': 'Nublado', 'icon': '03d', 'location': 'Oruro'
            },
            # Trinidad - Tropical, muy caluroso y húmedo
            (-14.83, -64.90): {
                'temp': 32, 'humidity': 80, 'wind': 12, 'clouds': 60,
                'desc': 'Nublado con posibilidad de lluvia', 'icon': '04d', 'location': 'Trinidad'
            },
            # Cobija - Amazónico, caluroso y muy húmedo
            (-11.03, -68.73): {
                'temp': 30, 'humidity': 85, 'wind': 8, 'clouds': 70,
                'desc': 'Muy nublado', 'icon': '04d', 'location': 'Cobija'
            }
        }
        
        # Buscar la ciudad más cercana
        min_dist = float('inf')
        selected_weather = None
        
        for (city_lat, city_lon), weather in city_weather.items():
            dist = ((lat - city_lat)**2 + (lon - city_lon)**2)**0.5
            if dist < min_dist:
                min_dist = dist
                selected_weather = weather
        
        # Si no se encuentra, usar Santa Cruz por defecto
        if not selected_weather:
            selected_weather = city_weather[(-17.78, -63.18)]
        
        temp = selected_weather['temp']
        
        return {
            'temperature': float(temp),
            'feels_like': float(temp + 2),
            'temp_min': float(temp - 5),
            'temp_max': float(temp + 5),
            'humidity': selected_weather['humidity'],
            'pressure': 1013,
            'wind_speed': float(selected_weather['wind']),
            'wind_direction': 180,
            'clouds': selected_weather['clouds'],
            'description': selected_weather['desc'],
            'icon': selected_weather['icon'],
            'sunrise': '06:30',
            'sunset': '18:45',
            'location': selected_weather['location'],
            'country': 'BO',
            'timestamp': datetime.now().isoformat(),
            'simulated': True
        }
    
    def _get_simulated_forecast(self, lat, lon, days):
        """Genera datos simulados de pronóstico basados en ubicación"""
        # Obtener clima base de la ciudad
        current = self._get_simulated_current_weather(lat, lon)
        base_temp = current['temperature']
        base_humidity = current['humidity']
        
        forecast = []
        base_date = datetime.now().date()
        
        # Variaciones realistas por día
        temp_variations = [0, 2, 1, -1, 3]
        rain_probs = [20, 30, 15, 40, 25]
        conditions = [
            ('Soleado', '01d'),
            ('Parcialmente nublado', '02d'),
            ('Despejado', '01d'),
            ('Nublado', '03d'),
            ('Parcialmente nublado', '02d')
        ]
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            temp_var = temp_variations[i % len(temp_variations)]
            desc, icon = conditions[i % len(conditions)]
            
            forecast.append({
                'date': date.isoformat(),
                'day_name': self._get_day_name(date),
                'temp_min': float(base_temp - 5 + temp_var),
                'temp_max': float(base_temp + 5 + temp_var),
                'humidity': base_humidity + (i * 2),
                'description': desc,
                'icon': icon,
                'wind_speed': current['wind_speed'] + (i * 2),
                'rain_probability': rain_probs[i % len(rain_probs)],
                'clouds': 30 + (i * 5),
                'simulated': True
            })
        
        return forecast


# Instancia global del servicio
weather_service = WeatherService()
