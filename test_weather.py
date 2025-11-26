#!/usr/bin/env python
"""Script para probar el sistema de clima"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from weather.weather_service import weather_service
from dotenv import load_dotenv

load_dotenv()

def test_weather():
    print("=" * 60)
    print("🌤️ PRUEBA DEL SISTEMA DE CLIMA")
    print("=" * 60)
    
    # Verificar API key
    api_key = os.getenv('OPENWEATHER_API_KEY')
    print(f"\n1. Verificando API Key...")
    if api_key:
        print(f"   ✅ API Key encontrada: {api_key[:20]}...")
        print(f"   📡 Usando datos reales de OpenWeatherMap")
    else:
        print(f"   ⚠️ No hay API Key")
        print(f"   🎭 Usando datos simulados")
    
    # Coordenadas de Santa Cruz, Bolivia
    lat, lon = -17.78, -63.18
    print(f"\n2. Ubicación de prueba:")
    print(f"   📍 Latitud: {lat}")
    print(f"   📍 Longitud: {lon}")
    print(f"   🌎 Santa Cruz, Bolivia")
    
    # Probar clima actual
    print(f"\n3. Obteniendo clima actual...")
    try:
        current = weather_service.get_current_weather(lat, lon)
        print(f"   ✅ Clima actual obtenido")
        print(f"   🌡️ Temperatura: {current['temperature']}°C")
        print(f"   💧 Humedad: {current['humidity']}%")
        print(f"   💨 Viento: {current['wind_speed']} km/h")
        print(f"   ☁️ Condiciones: {current['description']}")
        print(f"   📍 Ubicación: {current['location']}, {current['country']}")
        if current.get('simulated'):
            print(f"   🎭 (Datos simulados)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Probar pronóstico
    print(f"\n4. Obteniendo pronóstico...")
    try:
        forecast = weather_service.get_forecast(lat, lon, 5)
        print(f"   ✅ Pronóstico obtenido")
        print(f"   📅 Días: {len(forecast)}")
        for day in forecast[:3]:
            print(f"   • {day['day_name']}: {day['temp_max']}°/{day['temp_min']}° - {day['description']}")
            print(f"     🌧️ Prob. lluvia: {day['rain_probability']}%")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Probar datos agrícolas
    print(f"\n5. Obteniendo datos agrícolas...")
    try:
        agri_data = weather_service.get_agricultural_data(lat, lon)
        print(f"   ✅ Datos agrícolas obtenidos")
        
        # Alertas
        if agri_data['alerts']:
            print(f"\n   ⚠️ ALERTAS ({len(agri_data['alerts'])}):")
            for alert in agri_data['alerts']:
                print(f"   {alert['message']}")
        else:
            print(f"\n   ✅ Sin alertas")
        
        # Recomendaciones
        if agri_data['recommendations']:
            print(f"\n   💡 RECOMENDACIONES ({len(agri_data['recommendations'])}):")
            for rec in agri_data['recommendations'][:3]:
                print(f"   • {rec}")
        
        # Índices
        indices = agri_data['agricultural_index']
        print(f"\n   📊 ÍNDICES AGRÍCOLAS:")
        print(f"   • Necesidad de riego: {indices['irrigation_need']}/100")
        print(f"   • Condiciones fumigación: {indices['spray_conditions']}/100")
        print(f"   • Condiciones cosecha: {indices['harvest_conditions']}/100")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    
    if not api_key:
        print("\n💡 Para usar datos reales:")
        print("   1. Obtén API key gratis en: https://openweathermap.org/api")
        print("   2. Agrégala al .env: OPENWEATHER_API_KEY=tu_key")
        print("   3. Reinicia el servidor")
    
    print("\n📖 Endpoints disponibles:")
    print("   GET /api/weather/current/?lat=-17.78&lon=-63.18")
    print("   GET /api/weather/forecast/?lat=-17.78&lon=-63.18")
    print("   GET /api/weather/agricultural/?lat=-17.78&lon=-63.18")
    print("   GET /api/weather/parcel/<id>/")
    
    return True

if __name__ == "__main__":
    test_weather()
