from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from .models import User


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Registrar inicio de sesión en auditoría"""
    from audit.utils import log_audit
    log_audit(
        user=user,
        action='LOGIN',
        model_name='User',
        object_id=user.id,
        description=f'Usuario {user.username} inició sesión',
        ip_address=request.META.get('REMOTE_ADDR')
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Registrar cierre de sesión en auditoría"""
    if user:
        from audit.utils import log_audit
        log_audit(
            user=user,
            action='LOGOUT',
            model_name='User',
            object_id=user.id,
            description=f'Usuario {user.username} cerró sesión',
            ip_address=request.META.get('REMOTE_ADDR')
        )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """Registrar intento fallido de inicio de sesión"""
    from audit.utils import log_audit
    log_audit(
        user=None,
        action='LOGIN_FAILED',
        model_name='User',
        description=f'Intento fallido de inicio de sesión con username: {credentials.get("username")}',
        ip_address=request.META.get('REMOTE_ADDR') if request else None
    )
