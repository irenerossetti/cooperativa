from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AIRecommendation


@receiver(post_save, sender=AIRecommendation)
def log_recommendation_save(sender, instance, created, **kwargs):
    """Registrar creación de recomendación en auditoría"""
    from audit.utils import log_audit
    if created:
        log_audit(
            user=None,
            action='CREATE',
            model_name='AIRecommendation',
            object_id=instance.id,
            description=f'Recomendación IA generada: {instance.title}'
        )
