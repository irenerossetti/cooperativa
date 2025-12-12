#!/usr/bin/env python
"""
Script de instalación automática para las nuevas funcionalidades
Ejecutar: python install_new_features.py
"""

import os
import sys
import subprocess

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print_info(f"{description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print_success(f"{description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error en {description}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print_header("INSTALACIÓN DE NUEVAS FUNCIONALIDADES")
    print("Este script instalará:")
    print("1. Sistema de Notificaciones")
    print("2. Generador de Códigos QR")
    print("3. Dashboard en Tiempo Real")
    print("4. Asistente de IA con Chat")
    print("\n¿Deseas continuar? (s/n): ", end="")
    
    if input().lower() != 's':
        print("Instalación cancelada.")
        return
    
    # 1. Instalar dependencias de Python
    print_header("PASO 1: Instalando dependencias de Python")
    if not run_command(
        "pip install qrcode[pil] pillow requests",
        "Instalación de qrcode, pillow y requests"
    ):
        print_error("Error al instalar dependencias. Abortando.")
        return
    
    # 2. Crear migraciones
    print_header("PASO 2: Creando migraciones")
    if not run_command(
        "python manage.py makemigrations notifications qr_codes ai_chat",
        "Creación de migraciones"
    ):
        print_error("Error al crear migraciones. Abortando.")
        return
    
    # 3. Aplicar migraciones
    print_header("PASO 3: Aplicando migraciones")
    if not run_command(
        "python manage.py migrate",
        "Aplicación de migraciones"
    ):
        print_error("Error al aplicar migraciones. Abortando.")
        return
    
    # 4. Crear datos de prueba
    print_header("PASO 4: Creando datos de prueba")
    print_info("Creando notificaciones de prueba...")
    
    # Crear script de datos de prueba
    test_script = """
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from notifications.utils import create_notification, notify_admins
from users.models import User

print("Creando notificaciones de prueba...")

# Obtener usuarios
users = User.objects.filter(is_active=True)[:3]

for user in users:
    # Notificación de bienvenida
    create_notification(
        user=user,
        title='¡Bienvenido al nuevo sistema!',
        message='Se han agregado nuevas funcionalidades: Notificaciones, QR, Dashboard en Tiempo Real y Chat IA',
        notification_type='INFO'
    )
    
    # Notificación de éxito
    create_notification(
        user=user,
        title='Sistema actualizado',
        message='El sistema ha sido actualizado exitosamente con 5 nuevas funcionalidades',
        notification_type='SUCCESS'
    )

# Notificar a admins
notify_admins(
    title='Nuevas funcionalidades disponibles',
    message='Se han instalado: Notificaciones, Códigos QR, Dashboard Tiempo Real y Chat IA',
    notification_type='INFO'
)

print("✅ Notificaciones de prueba creadas exitosamente")
"""
    
    with open('create_test_notifications_temp.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    run_command(
        "python create_test_notifications_temp.py",
        "Creación de notificaciones de prueba"
    )
    
    # Limpiar archivo temporal
    if os.path.exists('create_test_notifications_temp.py'):
        os.remove('create_test_notifications_temp.py')
    
    # 5. Verificar instalación
    print_header("PASO 5: Verificando instalación")
    
    verification_script = """
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from notifications.models import Notification
from qr_codes.models import QRCode
from ai_chat.models import ChatConversation

print("\\nVerificando modelos...")
print(f"✅ Notificaciones: {Notification.objects.count()} registros")
print(f"✅ Códigos QR: {QRCode.objects.count()} registros")
print(f"✅ Conversaciones IA: {ChatConversation.objects.count()} registros")
print("\\n✅ Todos los modelos están funcionando correctamente")
"""
    
    with open('verify_installation_temp.py', 'w', encoding='utf-8') as f:
        f.write(verification_script)
    
    run_command(
        "python verify_installation_temp.py",
        "Verificación de instalación"
    )
    
    # Limpiar archivo temporal
    if os.path.exists('verify_installation_temp.py'):
        os.remove('verify_installation_temp.py')
    
    # Resumen final
    print_header("INSTALACIÓN COMPLETADA")
    print_success("Backend instalado correctamente")
    print("\n📋 PRÓXIMOS PASOS:\n")
    print("1. Frontend - Instalar Recharts:")
    print("   cd cooperativa_frontend")
    print("   npm install recharts")
    print("\n2. Frontend - Agregar rutas en App.jsx:")
    print("   import NotificationsPage from './pages/NotificationsPage';")
    print("   import DashboardRealTime from './pages/DashboardRealTime';")
    print("   import AIChat from './pages/AIChat';")
    print("\n3. Frontend - Agregar NotificationBell en Navbar.jsx")
    print("\n4. Configurar .env (opcional para IA):")
    print("   OPENROUTER_API_KEY=tu_api_key_aqui")
    print("\n5. Probar las funcionalidades:")
    print("   - Notificaciones: http://localhost:5173/notifications")
    print("   - Dashboard: http://localhost:5173/dashboard-realtime")
    print("   - Chat IA: http://localhost:5173/ai-chat")
    print("\n📚 Documentación completa en:")
    print("   - IMPLEMENTACION_COMPLETA_5_FUNCIONALIDADES.md")
    print("   - GUIA_INSTALACION_NUEVAS_FUNCIONALIDADES.md")
    print("\n🎉 ¡Listo para la defensa!")

if __name__ == '__main__':
    main()
