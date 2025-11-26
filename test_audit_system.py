"""
Script de prueba del sistema de auditoría
Demuestra cómo usar el sistema de logs y el acceso con llave de desarrollador
"""

import os
import sys
import django
import requests
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from audit.models import AuditLog
from users.models import User
from tenants.models import Organization


def get_client_ip(request=None):
    """Obtener IP del cliente"""
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    return '127.0.0.1'


def create_sample_audit_logs():
    """Crear logs de auditoría de ejemplo"""
    print("\n" + "="*60)
    print("CREANDO LOGS DE AUDITORÍA DE EJEMPLO")
    print("="*60)
    
    # Obtener usuarios y organizaciones
    users = User.objects.all()[:3]
    orgs = Organization.objects.all()[:2]
    
    if not users.exists():
        print("❌ No hay usuarios en el sistema")
        return
    
    if not orgs.exists():
        print("❌ No hay organizaciones en el sistema")
        return
    
    # Crear diferentes tipos de logs
    actions = [
        {
            'user': users[0],
            'action': AuditLog.LOGIN,
            'description': 'Usuario inició sesión exitosamente',
            'ip_address': '192.168.1.100',
        },
        {
            'user': users[0],
            'action': AuditLog.CREATE,
            'model_name': 'Product',
            'object_id': 1,
            'description': 'Creó un nuevo producto: Fertilizante NPK',
            'ip_address': '192.168.1.100',
        },
        {
            'user': users[1],
            'action': AuditLog.LOGIN_FAILED,
            'description': 'Intento fallido de inicio de sesión - contraseña incorrecta',
            'ip_address': '192.168.1.105',
        },
        {
            'user': users[1],
            'action': AuditLog.LOGIN,
            'description': 'Usuario inició sesión exitosamente',
            'ip_address': '192.168.1.105',
        },
        {
            'user': users[1],
            'action': AuditLog.UPDATE,
            'model_name': 'Partner',
            'object_id': 1,
            'description': 'Actualizó información del socio: Juan Pérez',
            'ip_address': '192.168.1.105',
        },
        {
            'user': users[2],
            'action': AuditLog.DELETE,
            'model_name': 'Campaign',
            'object_id': 5,
            'description': 'Eliminó campaña: Campaña Primavera 2024',
            'ip_address': '10.0.0.50',
        },
    ]
    
    created_logs = []
    for action_data in actions:
        log = AuditLog.objects.create(**action_data)
        created_logs.append(log)
        print(f"✅ Log creado: {log}")
    
    print(f"\n📊 Total de logs creados: {len(created_logs)}")
    print(f"📊 Total de logs en sistema: {AuditLog.objects.count()}")
    
    return created_logs


def test_audit_queries():
    """Probar consultas de auditoría"""
    print("\n" + "="*60)
    print("PROBANDO CONSULTAS DE AUDITORÍA")
    print("="*60)
    
    # 1. Todos los logs
    total = AuditLog.objects.count()
    print(f"\n1. Total de logs: {total}")
    
    # 2. Logs de login
    logins = AuditLog.objects.filter(action=AuditLog.LOGIN).count()
    print(f"2. Logs de inicio de sesión: {logins}")
    
    # 3. Logs de intentos fallidos
    failed = AuditLog.objects.filter(action=AuditLog.LOGIN_FAILED).count()
    print(f"3. Intentos fallidos de login: {failed}")
    
    # 4. Logs por usuario
    users = User.objects.all()[:3]
    for user in users:
        count = AuditLog.objects.filter(user=user).count()
        print(f"4. Logs de {user.username}: {count}")
    
    # 5. Logs recientes (últimos 5)
    print("\n5. Últimos 5 logs:")
    recent = AuditLog.objects.select_related('user').order_by('-timestamp')[:5]
    for log in recent:
        username = log.user.username if log.user else 'Sistema'
        print(f"   - [{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
              f"{username} - {log.get_action_display()} - IP: {log.ip_address}")


def test_developer_key_access():
    """Probar acceso con llave de desarrollador"""
    print("\n" + "="*60)
    print("PROBANDO ACCESO CON LLAVE DE DESARROLLADOR")
    print("="*60)
    
    # Verificar si existe la llave
    developer_key = os.getenv('AUDIT_DEVELOPER_KEY')
    
    if not developer_key:
        print("\n⚠️  AUDIT_DEVELOPER_KEY no está configurada en .env")
        print("   Para probar esta funcionalidad:")
        print("   1. Agrega AUDIT_DEVELOPER_KEY=tu-llave-secreta en .env")
        print("   2. Reinicia el servidor Django")
        print("   3. Ejecuta este script nuevamente")
        return
    
    print(f"\n✅ Llave de desarrollador configurada: {developer_key[:10]}...")
    
    # Simular petición HTTP
    base_url = "http://localhost:8000"
    endpoint = f"{base_url}/api/audit/developer-access/"
    
    print(f"\n📡 Endpoint: {endpoint}")
    print(f"🔑 Header: X-Developer-Key: {developer_key[:10]}...")
    
    print("\n💡 Para probar el endpoint, ejecuta:")
    print(f'\ncurl -H "X-Developer-Key: {developer_key}" \\')
    print(f'     {endpoint}')
    
    print("\n💡 O con filtros:")
    print(f'\ncurl -H "X-Developer-Key: {developer_key}" \\')
    print(f'     "{endpoint}?action=LOGIN&user=1"')


def show_security_features():
    """Mostrar características de seguridad implementadas"""
    print("\n" + "="*60)
    print("CARACTERÍSTICAS DE SEGURIDAD DEL SISTEMA DE AUDITORÍA")
    print("="*60)
    
    print("\n✅ REQUISITOS CUMPLIDOS:")
    print("   1. ✓ Registro de IP de la máquina")
    print("   2. ✓ Registro del usuario")
    print("   3. ✓ Registro de fecha y hora")
    print("   4. ✓ Registro de acción realizada")
    print("   5. ✓ Archivo confidencial (solo admin puede ver)")
    print("   6. ✓ Acceso especial con llave de desarrollador")
    
    print("\n🔒 PROTECCIONES IMPLEMENTADAS:")
    print("   • Solo lectura en Django Admin")
    print("   • No se pueden crear logs manualmente")
    print("   • No se pueden modificar logs existentes")
    print("   • No se pueden eliminar logs")
    print("   • API requiere autenticación + rol Admin")
    print("   • Aislamiento por organización (multi-tenant)")
    print("   • Acceso completo solo con llave de desarrollador")
    
    print("\n📊 INFORMACIÓN CAPTURADA:")
    print("   • IP Address (IPv4/IPv6)")
    print("   • Usuario (con relación a User)")
    print("   • Timestamp (fecha y hora exacta)")
    print("   • Acción (LOGIN, LOGOUT, CREATE, UPDATE, DELETE)")
    print("   • Modelo afectado")
    print("   • ID del objeto")
    print("   • Descripción detallada")
    print("   • User Agent (navegador/cliente)")
    
    print("\n🔐 LLAVE DE DESARROLLADOR:")
    developer_key = os.getenv('AUDIT_DEVELOPER_KEY')
    if developer_key:
        print(f"   ✅ Configurada: {developer_key[:10]}...")
        print("   ✅ Permite acceso completo sin restricciones")
        print("   ✅ Bypass de multi-tenancy")
    else:
        print("   ⚠️  No configurada")
        print("   💡 Agregar AUDIT_DEVELOPER_KEY en .env")


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("SISTEMA DE AUDITORÍA - PRUEBA COMPLETA")
    print("="*60)
    
    try:
        # 1. Mostrar características de seguridad
        show_security_features()
        
        # 2. Crear logs de ejemplo
        create_sample_audit_logs()
        
        # 3. Probar consultas
        test_audit_queries()
        
        # 4. Probar acceso con llave de desarrollador
        test_developer_key_access()
        
        print("\n" + "="*60)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
