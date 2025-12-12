"""
Signals para crear notificaciones automáticas cuando se crean alertas
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Alert
from notifications.models import Notification


@receiver(post_save, sender=Alert)
def create_notification_from_alert(sender, instance, created, **kwargs):
    """
    Crea una notificación automáticamente cuando se crea una alerta
    """
    # Solo crear notificación para alertas nuevas
    if not created:
        return
    
    # Solo crear notificación si la alerta está activa
    if not instance.is_active:
        return
    
    try:
        # Determinar el tipo de notificación según la severidad de la alerta
        notification_type_map = {
            'LOW': 'INFO',
            'MEDIUM': 'WARNING',
            'HIGH': 'ERROR',
            'CRITICAL': 'ERROR'
        }
        
        notification_type = notification_type_map.get(instance.severity, 'ALERT')
        
        # Crear título descriptivo
        alert_type_names = {
            'STOCK': 'Stock Bajo',
            'WEATHER': 'Alerta Climática',
            'HARVEST': 'Momento de Cosecha',
            'PRICE': 'Alerta de Precios',
            'TASK': 'Tarea Pendiente',
            'GENERAL': 'Alerta General'
        }
        
        # Para alertas de precio, usar el título original que incluye el producto
        if instance.alert_type == 'PRICE':
            title = f"⚠️ {instance.title}"
        else:
            title = f"⚠️ {alert_type_names.get(instance.alert_type, 'Alerta')}"
        
        # Crear mensaje descriptivo
        message = instance.message
        
        # Agregar información adicional si está disponible
        if instance.severity in ['HIGH', 'CRITICAL']:
            message = f"🔴 URGENTE: {message}"
        elif instance.severity == 'MEDIUM':
            message = f"🟡 ATENCIÓN: {message}"
        
        # Datos adicionales para la notificación
        extra_data = {
            'alert_id': instance.id,
            'alert_type': instance.alert_type,
            'severity': instance.severity,
            'source': 'alert_system'
        }
        
        # URL de acción según el tipo de alerta
        action_url = None
        if instance.alert_type == 'STOCK':
            action_url = '/inventory'
        elif instance.alert_type == 'HARVEST':
            action_url = '/production'
        elif instance.alert_type == 'WEATHER':
            action_url = '/weather'
        elif instance.alert_type == 'PRICE':
            action_url = '/market-analysis'
        
        # Obtener usuarios a notificar
        # Por defecto, notificar a todos los usuarios activos de la organización
        from users.models import User
        users_to_notify = User.objects.filter(
            partner__organization=instance.organization,
            is_active=True
        ).distinct()
        
        # Si no hay usuarios con partner, notificar a todos los usuarios de la org
        if not users_to_notify.exists():
            # Buscar usuarios por otros medios (esto depende de tu estructura)
            # Por ahora, crear notificación para el usuario que creó la alerta si existe
            if hasattr(instance, 'created_by') and instance.created_by:
                users_to_notify = [instance.created_by]
        
        # Crear notificación para cada usuario
        notifications_created = 0
        for user in users_to_notify:
            Notification.objects.create(
                user=user,
                organization=instance.organization,
                title=title,
                message=message,
                type=notification_type,
                extra_data=extra_data,
                action_url=action_url,
                alert=instance
            )
            notifications_created += 1
        
        print(f"✅ Creadas {notifications_created} notificaciones para la alerta: {instance.message}")
        
    except Exception as e:
        print(f"❌ Error al crear notificación desde alerta: {e}")
        # No lanzar excepción para no interrumpir la creación de la alerta
        pass
