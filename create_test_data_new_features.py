"""
Script para crear datos de prueba para las nuevas funcionalidades
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from tenants.models import Organization
from partners.models import Partner
from notifications.models import Notification, NotificationPreference
from events.models import Event, EventReminder
from goals.models import Goal, GoalMilestone
from ai_chat.models import ChatConversation, ChatMessage
from qr_codes.models import QRCode
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

print("🚀 Creando datos de prueba para nuevas funcionalidades...\n")

# 1. Obtener o crear organización de prueba
org, created = Organization.objects.get_or_create(
    slug='test-org',
    defaults={
        'name': 'Organización de Prueba',
        'email': 'test@example.com',
        'phone': '1234567890',
        'address': 'Calle Test 123',
        'is_active': True
    }
)
print(f"{'✅ Creada' if created else '✓ Usando'} organización: {org.name}")

# 2. Obtener o crear usuario de prueba
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)
if created:
    user.set_password('testpass123')
    user.save()
print(f"{'✅ Creado' if created else '✓ Usando'} usuario: {user.username}")

# 3. Obtener o crear comunidad
from partners.models import Community
community, created = Community.objects.get_or_create(
    name='Comunidad Test',
    organization=org,
    defaults={
        'description': 'Comunidad de prueba',
        'is_active': True
    }
)
print(f"{'✅ Creada' if created else '✓ Usando'} comunidad: {community.name}")

# 4. Obtener o crear partner
partner, created = Partner.objects.get_or_create(
    ci='12345678',
    organization=org,
    defaults={
        'first_name': 'Test',
        'last_name': 'Partner',
        'phone': '1234567890',
        'address': 'Calle Partner 456',
        'community': community,
        'user': user,
        'status': 'ACTIVE'
    }
)
print(f"{'✅ Creado' if created else '✓ Usando'} partner: {partner.full_name}")

print("\n" + "="*60)
print("📊 Creando datos de prueba...")
print("="*60 + "\n")

# 5. Notificaciones
print("📬 Notificaciones:")
notif_types = [
    ('INFO', 'Bienvenido al sistema', 'Gracias por unirte a nuestra cooperativa'),
    ('SUCCESS', 'Cosecha registrada', 'Tu cosecha de café ha sido registrada exitosamente'),
    ('WARNING', 'Pago pendiente', 'Tienes un pago pendiente por $500'),
]

for notif_type, title, message in notif_types:
    notif, created = Notification.objects.get_or_create(
        user=user,
        organization=org,
        title=title,
        defaults={
            'message': message,
            'type': notif_type,
            'read': False
        }
    )
    print(f"   {'✅' if created else '✓'} {title}")

# Preferencias de notificación
pref, created = NotificationPreference.objects.get_or_create(
    user=user,
    organization=org,
    defaults={
        'email_enabled': True,
        'push_enabled': True,
        'notify_sales': True,
        'notify_payments': True,
        'notify_stock': True
    }
)
print(f"   {'✅' if created else '✓'} Preferencias configuradas")

# 6. Eventos
print("\n📅 Eventos:")
event_data = [
    ('Reunión de Cooperativa', 'REUNION', 'Reunión mensual para discutir avances', 7),
    ('Capacitación en Cultivo', 'CAPACITACION', 'Taller sobre técnicas de cultivo sostenible', 14),
    ('Día de Campo', 'INSPECCION', 'Visita a parcelas demostrativas', 21),
]

for title, event_type, description, days_ahead in event_data:
    start_date = timezone.now() + timedelta(days=days_ahead)
    end_date = start_date + timedelta(hours=2)
    event, created = Event.objects.get_or_create(
        title=title,
        organization=org,
        defaults={
            'type': event_type,
            'description': description,
            'start_datetime': start_date,
            'end_datetime': end_date,
            'location': 'Sede de la Cooperativa',
            'created_by': user,
            'priority': 'MEDIUM'
        }
    )
    if created:
        event.participants.add(user)
        # Crear recordatorio
        EventReminder.objects.create(
            event=event,
            user=user,
            method='NOTIFICATION'
        )
    print(f"   {'✅' if created else '✓'} {title}")

# 7. Metas
print("\n🎯 Metas:")
goal_data = [
    ('Aumentar Producción', 'Incrementar la producción de café en 20%', 'PRODUCTION', 80, 'kg'),
    ('Mejorar Calidad', 'Alcanzar certificación de calidad premium', 'QUALITY', 60, 'puntos'),
    ('Incrementar Ventas', 'Aumentar ventas en 15%', 'SALES', 45, 'Bs'),
]

for name, description, goal_type, progress, unit in goal_data:
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=90)
    goal, created = Goal.objects.get_or_create(
        name=name,
        organization=org,
        defaults={
            'description': description,
            'type': goal_type,
            'start_date': start_date,
            'end_date': end_date,
            'target_value': 100,
            'current_value': progress,
            'unit': unit,
            'responsible': user,
            'status': 'IN_PROGRESS'
        }
    )
    if created:
        # Crear hitos
        GoalMilestone.objects.create(
            goal=goal,
            title=f'Hito 1: {name}',
            description='Primer avance significativo',
            target_date=start_date + timedelta(days=30),
            completed=True
        )
        GoalMilestone.objects.create(
            goal=goal,
            title=f'Hito 2: {name}',
            description='Segundo avance significativo',
            target_date=start_date + timedelta(days=60),
            completed=False
        )
    print(f"   {'✅' if created else '✓'} {name} ({progress}%)")

# 8. Conversaciones de Chat IA
print("\n💬 Chat IA:")
conv, created = ChatConversation.objects.get_or_create(
    user=user,
    organization=org,
    defaults={
        'title': 'Consulta sobre cultivo de café'
    }
)
if created:
    ChatMessage.objects.create(
        conversation=conv,
        role='user',
        content='¿Cuál es el mejor momento para cosechar café?'
    )
    ChatMessage.objects.create(
        conversation=conv,
        role='assistant',
        content='El mejor momento para cosechar café es cuando los frutos están completamente maduros, de color rojo intenso. Esto generalmente ocurre entre 6-8 meses después de la floración.'
    )
print(f"   {'✅' if created else '✓'} Conversación de ejemplo")

# 9. Códigos QR
print("\n📱 Códigos QR:")
qr_data = [
    ('product', 1, 'Café Premium Orgánico'),
    ('parcel', 1, 'Parcela La Esperanza'),
    ('partner', partner.id, f'Socio {partner.full_name}'),
]

for model_type, object_id, description in qr_data:
    qr, created = QRCode.objects.get_or_create(
        organization=org,
        model_type=model_type,
        object_id=object_id,
        defaults={
            'qr_data': f'{{"type": "{model_type}", "id": {object_id}, "description": "{description}"}}'
        }
    )
    print(f"   {'✅' if created else '✓'} {description}")

print("\n" + "="*60)
print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
print("="*60)
print(f"\n📋 Resumen:")
print(f"   • Organización: {org.name}")
print(f"   • Usuario: {user.username}")
print(f"   • Notificaciones: {Notification.objects.filter(organization=org).count()}")
print(f"   • Eventos: {Event.objects.filter(organization=org).count()}")
print(f"   • Metas: {Goal.objects.filter(organization=org).count()}")
print(f"   • Conversaciones: {ChatConversation.objects.filter(organization=org).count()}")
print(f"   • Códigos QR: {QRCode.objects.filter(organization=org).count()}")
print("\n🔑 Credenciales de prueba:")
print(f"   Usuario: testuser")
print(f"   Contraseña: testpass123")
print(f"   Organización: test-org")
