import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from audit.models import AuditLog
from users.models import User

# Obtener usuarios
users = list(User.objects.all())

if not users:
    print("No hay usuarios en el sistema")
    exit()

# IPs de ejemplo
ips = [
    '192.168.1.100',
    '192.168.1.101',
    '192.168.1.102',
    '10.0.0.50',
    '172.16.0.10',
]

# Acciones y descripciones de ejemplo
actions_data = [
    ('LOGIN', 'Inicio de sesión exitoso'),
    ('LOGOUT', 'Cierre de sesión'),
    ('CREATE', 'Creó un nuevo socio'),
    ('UPDATE', 'Actualizó información de parcela'),
    ('DELETE', 'Eliminó un registro de inventario'),
    ('CREATE', 'Registró una nueva campaña'),
    ('UPDATE', 'Modificó datos de labor agrícola'),
    ('LOGIN_FAILED', 'Intento fallido de inicio de sesión'),
]

# Modelos de ejemplo
models = ['Partner', 'Parcel', 'Campaign', 'InventoryItem', 'FarmActivity', 'HarvestedProduct']

# Crear 20 registros de auditoría
print("Creando registros de auditoría de prueba...")

for i in range(20):
    action, base_description = random.choice(actions_data)
    user = random.choice(users) if action != 'LOGIN_FAILED' else None
    model_name = random.choice(models) if action in ['CREATE', 'UPDATE', 'DELETE'] else ''
    
    # Fecha aleatoria en los últimos 30 días
    days_ago = random.randint(0, 30)
    timestamp = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
    
    log = AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=random.randint(1, 100) if model_name else None,
        description=f"{base_description} - {model_name if model_name else 'Sistema'}",
        ip_address=random.choice(ips),
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    )
    # No actualizar timestamp para mantener la IP
    
    print(f"✓ Registro {i+1}: {action} - {log.description} - IP: {log.ip_address}")

print(f"\n✅ Se crearon 20 registros de auditoría con IPs")
print(f"Total de registros en auditoría: {AuditLog.objects.count()}")
