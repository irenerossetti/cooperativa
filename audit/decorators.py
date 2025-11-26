"""
Decoradores para logging automático de auditoría
"""

from functools import wraps
from .models import AuditLog


def get_client_ip(request):
    """Obtener IP del cliente desde el request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """Obtener User Agent del cliente"""
    return request.META.get('HTTP_USER_AGENT', '')


def audit_log(action, model_name='', get_object_id=None, get_description=None):
    """
    Decorador para registrar automáticamente acciones en la auditoría.
    
    Args:
        action: Tipo de acción (AuditLog.CREATE, AuditLog.UPDATE, etc.)
        model_name: Nombre del modelo afectado
        get_object_id: Función para obtener el ID del objeto (recibe response)
        get_description: Función para obtener la descripción (recibe request, response)
    
    Ejemplo de uso:
        @audit_log(
            action=AuditLog.CREATE,
            model_name='Product',
            get_object_id=lambda response: response.data.get('id'),
            get_description=lambda req, res: f"Creó producto: {res.data.get('name')}"
        )
        def create(self, request, *args, **kwargs):
            return super().create(request, *args, **kwargs)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # Ejecutar la función original
            response = func(self, request, *args, **kwargs)
            
            # Solo registrar si la operación fue exitosa (2xx)
            if 200 <= response.status_code < 300:
                try:
                    # Obtener información del objeto
                    object_id = None
                    if get_object_id:
                        object_id = get_object_id(response)
                    
                    # Obtener descripción
                    description = ''
                    if get_description:
                        description = get_description(request, response)
                    elif hasattr(response, 'data'):
                        description = f"Acción {action} en {model_name}"
                    
                    # Crear log de auditoría
                    AuditLog.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        action=action,
                        model_name=model_name,
                        object_id=object_id,
                        description=description,
                        ip_address=get_client_ip(request),
                        user_agent=get_user_agent(request)
                    )
                except Exception as e:
                    # No fallar la operación si el logging falla
                    print(f"Error al registrar auditoría: {e}")
            
            return response
        return wrapper
    return decorator


def audit_login(func):
    """
    Decorador específico para registrar intentos de login.
    
    Ejemplo de uso:
        @audit_login
        def post(self, request, *args, **kwargs):
            return super().post(request, *args, **kwargs)
    """
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        
        try:
            username = request.data.get('username', 'unknown')
            
            if 200 <= response.status_code < 300:
                # Login exitoso
                AuditLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    action=AuditLog.LOGIN,
                    description=f"Usuario {username} inició sesión exitosamente",
                    ip_address=get_client_ip(request),
                    user_agent=get_user_agent(request)
                )
            else:
                # Login fallido
                AuditLog.objects.create(
                    user=None,
                    action=AuditLog.LOGIN_FAILED,
                    description=f"Intento fallido de inicio de sesión para usuario: {username}",
                    ip_address=get_client_ip(request),
                    user_agent=get_user_agent(request)
                )
        except Exception as e:
            print(f"Error al registrar auditoría de login: {e}")
        
        return response
    return wrapper


def audit_logout(func):
    """
    Decorador específico para registrar logout.
    
    Ejemplo de uso:
        @audit_logout
        def post(self, request, *args, **kwargs):
            return super().post(request, *args, **kwargs)
    """
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        # Guardar usuario antes del logout
        user = request.user if request.user.is_authenticated else None
        username = user.username if user else 'unknown'
        
        response = func(self, request, *args, **kwargs)
        
        try:
            if 200 <= response.status_code < 300:
                AuditLog.objects.create(
                    user=user,
                    action=AuditLog.LOGOUT,
                    description=f"Usuario {username} cerró sesión",
                    ip_address=get_client_ip(request),
                    user_agent=get_user_agent(request)
                )
        except Exception as e:
            print(f"Error al registrar auditoría de logout: {e}")
        
        return response
    return wrapper


# Ejemplo de uso en ViewSets:
"""
from audit.decorators import audit_log, audit_login, audit_logout
from audit.models import AuditLog

class ProductViewSet(viewsets.ModelViewSet):
    
    @audit_log(
        action=AuditLog.CREATE,
        model_name='Product',
        get_object_id=lambda response: response.data.get('id'),
        get_description=lambda req, res: f"Creó producto: {res.data.get('name')}"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @audit_log(
        action=AuditLog.UPDATE,
        model_name='Product',
        get_object_id=lambda response: response.data.get('id'),
        get_description=lambda req, res: f"Actualizó producto: {res.data.get('name')}"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @audit_log(
        action=AuditLog.DELETE,
        model_name='Product',
        get_object_id=lambda response: kwargs.get('pk'),
        get_description=lambda req, res: f"Eliminó producto ID: {kwargs.get('pk')}"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class LoginView(APIView):
    
    @audit_login
    def post(self, request, *args, **kwargs):
        # Lógica de login
        pass


class LogoutView(APIView):
    
    @audit_logout
    def post(self, request, *args, **kwargs):
        # Lógica de logout
        pass
"""
