"""
Mixins para agregar auditoría automática a ViewSets
"""

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


class AuditMixin:
    """
    Mixin para agregar auditoría automática a ViewSets.
    
    Uso:
        class MyViewSet(AuditMixin, viewsets.ModelViewSet):
            audit_model_name = 'MyModel'  # Nombre del modelo para auditoría
            ...
    """
    
    audit_model_name = None  # Debe ser definido en la clase que usa el mixin
    
    def get_audit_model_name(self):
        """Obtener el nombre del modelo para auditoría"""
        if self.audit_model_name:
            return self.audit_model_name
        # Intentar obtener del serializer
        if hasattr(self, 'serializer_class'):
            return self.serializer_class.Meta.model.__name__
        return 'Unknown'
    
    def get_object_description(self, obj):
        """
        Obtener descripción del objeto para auditoría.
        Puede ser sobrescrito en subclases.
        """
        if hasattr(obj, 'name'):
            return str(obj.name)
        elif hasattr(obj, 'first_name') and hasattr(obj, 'last_name'):
            return f"{obj.first_name} {obj.last_name}"
        elif hasattr(obj, 'username'):
            return str(obj.username)
        elif hasattr(obj, 'title'):
            return str(obj.title)
        return f"ID: {obj.id if hasattr(obj, 'id') else 'unknown'}"
    
    def create_audit_log(self, action, obj=None, description=None):
        """Crear registro de auditoría"""
        try:
            if description is None and obj:
                obj_desc = self.get_object_description(obj)
                action_text = {
                    AuditLog.CREATE: 'Creó',
                    AuditLog.UPDATE: 'Actualizó',
                    AuditLog.DELETE: 'Eliminó',
                }.get(action, 'Modificó')
                description = f"{action_text} {self.get_audit_model_name()}: {obj_desc}"
            
            AuditLog.objects.create(
                user=self.request.user if self.request.user.is_authenticated else None,
                action=action,
                model_name=self.get_audit_model_name(),
                object_id=obj.id if obj and hasattr(obj, 'id') else None,
                description=description or f"Acción {action} en {self.get_audit_model_name()}",
                ip_address=get_client_ip(self.request),
                user_agent=get_user_agent(self.request)
            )
        except Exception as e:
            # No fallar la operación si el logging falla
            print(f"Error al registrar auditoría: {e}")
    
    def perform_create(self, serializer):
        """Override para agregar auditoría en creación"""
        instance = serializer.save()
        self.create_audit_log(AuditLog.CREATE, instance)
        return instance
    
    def perform_update(self, serializer):
        """Override para agregar auditoría en actualización"""
        instance = serializer.save()
        self.create_audit_log(AuditLog.UPDATE, instance)
        return instance
    
    def perform_destroy(self, instance):
        """Override para agregar auditoría en eliminación"""
        # Guardar descripción antes de eliminar
        description = f"Eliminó {self.get_audit_model_name()}: {self.get_object_description(instance)}"
        obj_id = instance.id
        
        # Eliminar el objeto
        instance.delete()
        
        # Crear log después de eliminar
        try:
            AuditLog.objects.create(
                user=self.request.user if self.request.user.is_authenticated else None,
                action=AuditLog.DELETE,
                model_name=self.get_audit_model_name(),
                object_id=obj_id,
                description=description,
                ip_address=get_client_ip(self.request),
                user_agent=get_user_agent(self.request)
            )
        except Exception as e:
            print(f"Error al registrar auditoría de eliminación: {e}")
