from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """Manejador personalizado de excepciones"""
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': True,
            'message': response.data.get('detail', 'Error en la solicitud'),
            'data': response.data
        }
        response.data = custom_response_data

    return response
