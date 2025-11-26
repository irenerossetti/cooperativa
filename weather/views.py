from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .weather_service import weather_service
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_weather(request):
    """
    Obtiene el clima actual para una ubicación
    
    Query params:
        lat: Latitud (default: -17.78 Santa Cruz)
        lon: Longitud (default: -63.18 Santa Cruz)
    """
    try:
        lat = float(request.GET.get('lat', -17.78))
        lon = float(request.GET.get('lon', -63.18))
        
        weather_data = weather_service.get_current_weather(lat, lon)
        
        return Response({
            'success': True,
            'data': weather_data
        })
    
    except ValueError:
        return Response(
            {'error': 'Latitud y longitud deben ser números válidos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error al obtener clima actual: {e}")
        return Response(
            {'error': 'Error al obtener datos del clima'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_forecast(request):
    """
    Obtiene el pronóstico del clima
    
    Query params:
        lat: Latitud (default: -17.78 Santa Cruz)
        lon: Longitud (default: -63.18 Santa Cruz)
        days: Número de días (default: 5, max: 5)
    """
    try:
        lat = float(request.GET.get('lat', -17.78))
        lon = float(request.GET.get('lon', -63.18))
        days = min(int(request.GET.get('days', 5)), 5)
        
        forecast_data = weather_service.get_forecast(lat, lon, days)
        
        return Response({
            'success': True,
            'data': forecast_data,
            'days': len(forecast_data)
        })
    
    except ValueError:
        return Response(
            {'error': 'Parámetros inválidos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error al obtener pronóstico: {e}")
        return Response(
            {'error': 'Error al obtener pronóstico del clima'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_agricultural_data(request):
    """
    Obtiene datos del clima específicos para agricultura
    Incluye alertas y recomendaciones
    
    Query params:
        lat: Latitud (default: -17.78 Santa Cruz)
        lon: Longitud (default: -63.18 Santa Cruz)
    """
    try:
        lat = float(request.GET.get('lat', -17.78))
        lon = float(request.GET.get('lon', -63.18))
        
        agricultural_data = weather_service.get_agricultural_data(lat, lon)
        
        return Response({
            'success': True,
            'data': agricultural_data
        })
    
    except ValueError:
        return Response(
            {'error': 'Latitud y longitud deben ser números válidos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error al obtener datos agrícolas: {e}")
        return Response(
            {'error': 'Error al obtener datos agrícolas del clima'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weather_by_parcel(request, parcel_id):
    """
    Obtiene el clima para una parcela específica
    
    Args:
        parcel_id: ID de la parcela
    """
    try:
        from parcels.models import Parcel
        
        parcel = Parcel.objects.get(id=parcel_id)
        
        # Usar coordenadas de la parcela si están disponibles
        lat = parcel.latitude if hasattr(parcel, 'latitude') and parcel.latitude else -17.78
        lon = parcel.longitude if hasattr(parcel, 'longitude') and parcel.longitude else -63.18
        
        agricultural_data = weather_service.get_agricultural_data(lat, lon)
        
        return Response({
            'success': True,
            'parcel': {
                'id': parcel.id,
                'code': parcel.code,
                'name': parcel.name
            },
            'data': agricultural_data
        })
    
    except Parcel.DoesNotExist:
        return Response(
            {'error': 'Parcela no encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error al obtener clima de parcela: {e}")
        return Response(
            {'error': 'Error al obtener clima de la parcela'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
