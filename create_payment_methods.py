import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sales.models import PaymentMethod

print("=" * 60)
print("CREANDO MÉTODOS DE PAGO")
print("=" * 60)

payment_methods = [
    {
        'name': 'CASH',
        'description': 'Pago en efectivo',
        'is_active': True,
        'requires_reference': False
    },
    {
        'name': 'BANK_TRANSFER',
        'description': 'Transferencia bancaria',
        'is_active': True,
        'requires_reference': True
    },
    {
        'name': 'CHECK',
        'description': 'Pago con cheque',
        'is_active': True,
        'requires_reference': True
    },
    {
        'name': 'CREDIT_CARD',
        'description': 'Tarjeta de crédito',
        'is_active': True,
        'requires_reference': False
    },
    {
        'name': 'DEBIT_CARD',
        'description': 'Tarjeta de débito',
        'is_active': True,
        'requires_reference': False
    },
    {
        'name': 'QR',
        'description': 'Pago por código QR',
        'is_active': True,
        'requires_reference': True
    },
]

created = 0
updated = 0

for pm_data in payment_methods:
    pm, created_flag = PaymentMethod.objects.get_or_create(
        name=pm_data['name'],
        defaults=pm_data
    )
    
    if created_flag:
        print(f"✅ Creado: {pm.get_name_display()}")
        created += 1
    else:
        # Actualizar
        pm.description = pm_data['description']
        pm.is_active = pm_data['is_active']
        pm.requires_reference = pm_data['requires_reference']
        pm.save()
        print(f"ℹ️  Actualizado: {pm.get_name_display()}")
        updated += 1

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"✅ Métodos creados: {created}")
print(f"ℹ️  Métodos actualizados: {updated}")
print(f"📋 Total de métodos: {PaymentMethod.objects.count()}")
print("\n🎉 ¡Métodos de pago listos!")
print("=" * 60)
