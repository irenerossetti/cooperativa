from .models import Notification, NotificationPreference
from django.contrib.auth import get_user_model

User = get_user_model()


def create_notification(user, title, message, notification_type='INFO', extra_data=None, action_url=None, alert=None):
    """
    Función helper para crear notificaciones fácilmente
    
    Args:
        user: Usuario destinatario
        title: Título de la notificación
        message: Mensaje de la notificación
        notification_type: Tipo de notificación (INFO, SUCCESS, WARNING, ERROR, etc.)
        extra_data: Datos adicionales en formato dict
        action_url: URL de acción opcional
        alert: Alerta relacionada (opcional)
    
    Returns:
        Notification: Instancia de la notificación creada
    """
    # Verificar preferencias del usuario
    try:
        preferences = NotificationPreference.objects.get(user=user)
        
        # Verificar si el usuario tiene habilitadas las notificaciones de este tipo
        type_mapping = {
            'SALE': preferences.notify_sales,
            'PAYMENT': preferences.notify_payments,
            'STOCK': preferences.notify_stock,
            'REQUEST': preferences.notify_requests,
            'ALERT': preferences.notify_alerts,
            'TASK': preferences.notify_tasks,
        }
        
        if notification_type in type_mapping and not type_mapping[notification_type]:
            return None  # Usuario no quiere este tipo de notificación
            
    except NotificationPreference.DoesNotExist:
        # Si no hay preferencias, crear notificación de todos modos
        pass
    
    # Obtener organización del usuario o de la alerta
    organization = None
    if alert and hasattr(alert, 'organization'):
        organization = alert.organization
    elif hasattr(user, 'partner') and user.partner:
        organization = user.partner.organization
    
    notification = Notification.objects.create(
        user=user,
        organization=organization,
        title=title,
        message=message,
        type=notification_type,
        extra_data=extra_data,
        action_url=action_url,
        alert=alert
    )
    
    return notification


def notify_admins(title, message, notification_type='INFO', extra_data=None):
    """
    Envía notificación a todos los administradores
    """
    from users.models import Role
    
    admin_role = Role.objects.filter(name='Administrador').first()
    if not admin_role:
        return []
    
    admin_users = User.objects.filter(role=admin_role, is_active=True)
    
    notifications = []
    for user in admin_users:
        notification = create_notification(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            extra_data=extra_data
        )
        if notification:
            notifications.append(notification)
    
    return notifications


def notify_user_group(users, title, message, notification_type='INFO', extra_data=None):
    """
    Envía notificación a un grupo de usuarios
    """
    notifications = []
    for user in users:
        notification = create_notification(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            extra_data=extra_data
        )
        if notification:
            notifications.append(notification)
    
    return notifications


# Funciones específicas por tipo de evento

def notify_new_sale(sale):
    """Notifica cuando se crea una nueva venta"""
    return notify_admins(
        title='Nueva venta registrada',
        message=f'Se ha registrado una nueva venta por Bs. {sale.total_amount}',
        notification_type='SALE',
        extra_data={'sale_id': sale.id, 'amount': float(sale.total_amount)}
    )


def notify_low_stock(item):
    """Notifica cuando un item tiene stock bajo"""
    return notify_admins(
        title='Alerta de stock bajo',
        message=f'El item "{item.name}" tiene stock bajo ({item.current_stock} unidades)',
        notification_type='STOCK',
        extra_data={'item_id': item.id, 'stock': item.current_stock}
    )


def notify_payment_received(payment):
    """Notifica cuando se recibe un pago"""
    # Notificar al socio
    if hasattr(payment, 'partner') and payment.partner:
        create_notification(
            user=payment.partner.user if payment.partner.user else None,
            title='Pago recibido',
            message=f'Se ha registrado tu pago de Bs. {payment.amount}',
            notification_type='PAYMENT',
            extra_data={'payment_id': payment.id, 'amount': float(payment.amount)}
        )
    
    # Notificar a admins
    return notify_admins(
        title='Nuevo pago registrado',
        message=f'Se ha recibido un pago de Bs. {payment.amount}',
        notification_type='PAYMENT',
        extra_data={'payment_id': payment.id, 'amount': float(payment.amount)}
    )


def notify_new_request(request_obj):
    """Notifica cuando se crea una nueva solicitud"""
    return notify_admins(
        title='Nueva solicitud',
        message=f'Nueva solicitud de {request_obj.partner.full_name}: {request_obj.subject}',
        notification_type='REQUEST',
        extra_data={'request_id': request_obj.id}
    )


def notify_task_assigned(task, user):
    """Notifica cuando se asigna una tarea"""
    return create_notification(
        user=user,
        title='Nueva tarea asignada',
        message=f'Se te ha asignado la tarea: {task.title}',
        notification_type='TASK',
        extra_data={'task_id': task.id},
        action_url=f'/tasks/{task.id}'
    )
