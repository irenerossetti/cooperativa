from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FieldExpense


@receiver(post_save, sender=FieldExpense)
def update_profitability_on_expense(sender, instance, created, **kwargs):
    """Actualizar rentabilidad cuando se registra un gasto"""
    if created:
        from .models import ParcelProfitability
        profitability, created = ParcelProfitability.objects.get_or_create(
            parcel=instance.parcel,
            campaign=instance.campaign
        )
        # Recalcular gastos totales
        total_expenses = instance.parcel.field_expenses.filter(
            campaign=instance.campaign
        ).aggregate(models.Sum('total_cost'))['total_cost__sum'] or 0
        
        profitability.total_expenses = total_expenses
        profitability.calculate_profitability()
