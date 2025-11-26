from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import Organization
import threading

# Thread-local storage para el tenant actual
_thread_locals = threading.local()


def get_current_organization():
    """Obtiene la organización actual del thread-local storage"""
    return getattr(_thread_locals, 'organization', None)


def set_current_organization(organization):
    """Establece la organización actual en el thread-local storage"""
    _thread_locals.organization = organization


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware que detecta y establece el tenant actual basado en:
    1. Subdominio (ej: cooperativa1.tuapp.com)
    2. Header HTTP X-Organization-Subdomain
    3. Query parameter ?org=subdomain
    """
    
    def process_request(self, request):
        organization = None
        
        # Método 1: Detectar por subdominio
        host = request.get_host().split(':')[0]  # Remover puerto si existe
        parts = host.split('.')
        
        # Si hay subdominio (ej: cooperativa1.localhost o cooperativa1.tuapp.com)
        if len(parts) > 2 or (len(parts) == 2 and parts[0] not in ['localhost', '127']):
            subdomain = parts[0]
            if subdomain not in ['www', 'api', 'admin']:
                try:
                    organization = Organization.objects.get(
                        subdomain=subdomain,
                        is_active=True
                    )
                except Organization.DoesNotExist:
                    pass
        
        # Método 2: Header HTTP (útil para APIs y desarrollo)
        if not organization:
            subdomain = request.headers.get('X-Organization-Subdomain')
            if subdomain:
                try:
                    organization = Organization.objects.get(
                        subdomain=subdomain,
                        is_active=True
                    )
                except Organization.DoesNotExist:
                    pass
        
        # Método 3: Query parameter (útil para desarrollo)
        if not organization:
            subdomain = request.GET.get('org')
            if subdomain:
                try:
                    organization = Organization.objects.get(
                        subdomain=subdomain,
                        is_active=True
                    )
                except Organization.DoesNotExist:
                    pass
        
        # Establecer la organización en el thread-local y en el request
        set_current_organization(organization)
        request.organization = organization
        
        # Si no se encontró organización y la ruta requiere tenant, retornar error
        # (excepto para rutas públicas como login, registro, etc.)
        public_paths = [
            '/api/auth/',
            '/api/register/',
            '/admin/',
            '/api/tenants/register/',
            '/api/tenants/my-organizations/',
        ]
        is_public = any(request.path.startswith(path) for path in public_paths)
        
        if not organization and not is_public and request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'Organización no encontrada',
                'detail': 'Debe especificar una organización válida mediante subdominio, header X-Organization-Subdomain, o parámetro ?org='
            }, status=400)
        
        return None
    
    def process_response(self, request, response):
        # Limpiar el thread-local después de la request
        set_current_organization(None)
        return response
