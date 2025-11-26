"""
Script para generar logs de auditoría de prueba
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from audit.models import AuditLog
from users.models import User
from tenants.models import Organization
from django.utils import timezone

def generar_logs_prueba():
    """Generar logs de auditoría de prueba"""
    print("\n" + "="*60)
    print("GENERANDO LOGS DE AUDITORÍA DE PRUEBA")
    print("="*60)
    
    # Obtener la organización
    try:
        org = Organization.objects.filter(is_active=True).first()
        if not org:
            print("\n❌ No se encontró ninguna organización activa")
            print("   Crea una organización primero")
            return
        
        print(f"\n✅ Organización encontrada: {org.name}")
        
        # Obtener el usuario admin
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            admin = User.objects.filter(username='admin').first()
        
        if not admin:
            print("\n❌ No se encontró usuario admin")
            print("   Crea un usuario admin primero")
            return
        
        print(f"✅ Usuario encontrado: {admin.username}")
        
        # Generar logs de ejemplo
        logs_data = [
            {
                'action': AuditLog.CREATE,
                'model_name': 'Partner',
                'description': 'Creó socio: Juan Pérez García',
                'object_id': 1
            },
            {
                'action': AuditLog.UPDATE,
                'model_name': 'Partner',
                'description': 'Actualizó socio: María López',
                'object_id': 2
            },
            {
                'action': AuditLog.CREATE,
                'model_name': 'Parcel',
                'description': 'Creó parcela: Parcela Norte',
                'object_id': 1
            },
            {
                'action': AuditLog.UPDATE,
                'model_name': 'User',
                'description': 'Actualizó usuario: cliente1',
                'object_id': 3
            },
            {
                'action': AuditLog.DELETE,
                'model_name': 'Role',
                'description': 'Eliminó rol: Rol Temporal',
                'object_id': 5
            },
            {
                'action': AuditLog.CREATE,
                'model_name': 'Order',
                'description': 'Creó pedido #1001',
                'object_id': 1
            },
            {
                'action': AuditLog.UPDATE,
                'model_name': 'Order',
                'description': 'Actualizó pedido #1001 - Estado: Confirmado',
                'object_id': 1
            },
            {
                'action': AuditLog.CREATE,
                'model_name': 'Customer',
                'description': 'Creó cliente: Empresa ABC S.A.',
                'object_id': 1
            },
        ]
        
        created_count = 0
        for log_data in logs_data:
            log = AuditLog(
                user=admin,
                action=log_data['action'],
                model_name=log_data['model_name'],
                object_id=log_data.get('object_id'),
                description=log_data['description'],
                ip_address='127.0.0.1',
                user_agent='Mozilla/5.0 (Test Script)',
                organization=org
            )
            log.save()
            created_count += 1
            print(f"  ✓ {log_data['description']}")
        
        print(f"\n✅ Se crearon {created_count} logs de prueba")
        print("\n" + "="*60)
        print("Ahora puedes ver estos logs en la página de Auditoría")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    generar_logs_prueba()
