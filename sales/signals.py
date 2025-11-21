from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, Payment


@receiver(post_save, sender=Order)
def log_order_save(sender, instance, created, **kwargs):
    """Registrar creación/actualización de pedido en auditoría"""
    from audit.utils import log_audit
    action = 'CREATE' if created else 'UPDATE'
    description = f'Pedido {instance.order_number} - {instance.customer.name} {"creado" if created else "actualizado"}'
    
    log_audit(
        user=instance.created_by if created else None,
        action=action,
        model_name='Order',
        object_id=instance.id,
        description=description
    )


@receiver(post_save, sender=Payment)
def update_order_status_on_payment(sender, instance, created, **kwargs):
    """Actualizar estado del pedido cuando se registra un pago"""
    if created and instance.status == 'COMPLETED':
        order = instance.order
        total_paid = sum(p.amount for p in order.payments.filter(status='COMPLETED'))
        
        if total_paid >= order.total:
            order.status = 'PAID'
            order.save()
