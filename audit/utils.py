from .models import AuditLog


def log_audit(user=None, action='', model_name='', object_id=None, description='', 
              ip_address=None, user_agent=''):
    """Función auxiliar para registrar eventos en la auditoría"""
    try:
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent
        )
    except Exception as e:
        # Log error but don't break the application
        print(f"Error logging audit: {e}")
