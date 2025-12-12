from django.db.models.signals import post_save
from django.dispatch import receiver
from alerts.models import Alert
from .utils import create_notification


@receiver(post_save, sender=Alert)
def create_notification_from_alert(sender, instance, created, **kwargs):
    """
    Crea notificaciones automáticamente cuando se crea una alerta
    """
    if created:
        # Mapear severidad de alerta a tipo de notificación
        severity_to_type = {
            'LOW': 'INFO',
            'MEDIUM': 'WARNING',
            'HIGH': 'WARNING',
            'CRITICAL': 'ERROR',
        }
        
        notification_type = severity_to_type.get(instance.severity, 'ALERT')
        
        # Si la alerta tiene un usuario específico
        if instance.target_user:
            create_notification(
                user=instance.target_user,
                title=instance.title,
                message=instance.message,
                notification_type=notification_type,
                alert=instance,
                extra_data=instance.data
            )
        else:
            # Crear notificación para todos los usuarios activos de la organización
            from users.models import User
            users = User.objects.filter(
                partner__organization=instance.organization,
                is_active=True
            ).distinct()
            
            for user in users:
                create_notification(
                    user=user,
                    title=instance.title,
                    message=instance.message,
                    notification_type=notification_type,
                    alert=instance,
                    extra_data=instance.data
                )
