"""
Comando para crear notificaciones de alertas activas existentes
"""
from django.core.management.base import BaseCommand
from alerts.models import Alert
from notifications.models import Notification
from users.models import User


class Command(BaseCommand):
    help = 'Crea notificaciones para todas las alertas activas que no tienen notificación'

    def handle(self, *args, **options):
        self.stdout.write('🔔 Creando notificaciones de alertas activas...\n')
        
        # Obtener alertas activas que no han sido leídas
        active_alerts = Alert.objects.filter(
            is_active=True,
            is_read=False
        )
        
        total_alerts = active_alerts.count()
        self.stdout.write(f'📊 Alertas activas encontradas: {total_alerts}\n')
        
        if total_alerts == 0:
            self.stdout.write(self.style.WARNING('No hay alertas activas para procesar.'))
            return
        
        notifications_created = 0
        notifications_skipped = 0
        
        for alert in active_alerts:
            # Verificar si ya existe una notificación para esta alerta
            existing_notification = Notification.objects.filter(
                alert=alert,
                organization=alert.organization
            ).exists()
            
            if existing_notification:
                notifications_skipped += 1
                continue
            
            # Determinar tipo de notificación
            notification_type_map = {
                'LOW': 'INFO',
                'MEDIUM': 'WARNING',
                'HIGH': 'ERROR',
                'CRITICAL': 'ERROR'
            }
            notification_type = notification_type_map.get(alert.severity, 'ALERT')
            
            # Crear título
            alert_type_names = {
                'STOCK': 'Stock Bajo',
                'WEATHER': 'Alerta Climática',
                'HARVEST': 'Momento de Cosecha',
                'PRICE': 'Alerta de Precios',
                'TASK': 'Tarea Pendiente',
                'GENERAL': 'Alerta General'
            }
            title = f"⚠️ {alert_type_names.get(alert.alert_type, 'Alerta')}"
            
            # Crear mensaje
            message = alert.message
            if alert.severity in ['HIGH', 'CRITICAL']:
                message = f"🔴 URGENTE: {message}"
            elif alert.severity == 'MEDIUM':
                message = f"🟡 ATENCIÓN: {message}"
            
            # Datos adicionales
            extra_data = {
                'alert_id': alert.id,
                'alert_type': alert.alert_type,
                'severity': alert.severity,
                'source': 'alert_system'
            }
            
            # URL de acción
            action_url = None
            if alert.alert_type == 'STOCK':
                action_url = '/inventory'
            elif alert.alert_type == 'HARVEST':
                action_url = '/production'
            elif alert.alert_type == 'WEATHER':
                action_url = '/weather'
            elif alert.alert_type == 'PRICE':
                action_url = '/market-analysis'
            
            # Obtener usuarios a notificar
            users_to_notify = User.objects.filter(
                partner__organization=alert.organization,
                is_active=True
            ).distinct()
            
            # Crear notificación para cada usuario
            for user in users_to_notify:
                Notification.objects.create(
                    user=user,
                    organization=alert.organization,
                    title=title,
                    message=message,
                    type=notification_type,
                    extra_data=extra_data,
                    action_url=action_url,
                    alert=alert
                )
                notifications_created += 1
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso completado'))
        self.stdout.write(f'📊 Notificaciones creadas: {notifications_created}')
        self.stdout.write(f'⏭️  Notificaciones omitidas (ya existían): {notifications_skipped}')
        self.stdout.write('='*60)
