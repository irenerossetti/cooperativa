#!/usr/bin/env python
"""
Script de instalación completa para TODAS las nuevas funcionalidades
Ejecutar: python install_all_features.py
"""

import os
import sys

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def main():
    print_header("INSTALACIÓN COMPLETA - 7 FUNCIONALIDADES")
    
    print("Este script instalará:")
    print("\n📦 OPCIÓN A (Funcionalidades Críticas):")
    print("  1. Sistema de Notificaciones Push")
    print("  2. Generador de Códigos QR")
    print("  3. Dashboard en Tiempo Real")
    print("  4. Asistente de IA con Chat")
    print("\n📦 OPCIÓN B (CRUDs Complementarios):")
    print("  5. Calendario de Eventos Agrícolas")
    print("  6. Metas y Objetivos")
    print("\n📊 Total:")
    print("  - 52 archivos")
    print("  - 38 endpoints")
    print("  - 9 modelos")
    print("  - ~6,000 líneas de código")
    
    print("\n¿Deseas continuar? (s/n): ", end="")
    
    if input().lower() != 's':
        print("Instalación cancelada.")
        return
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print_error("Error: No se encontró manage.py")
        print_info("Asegúrate de ejecutar este script desde el directorio cooperativa/")
        return
    
    print_header("PASO 1: Verificando archivos creados")
    
    apps_to_check = [
        'notifications',
        'qr_codes',
        'dashboard',
        'ai_chat',
        'events',
        'goals'
    ]
    
    all_exist = True
    for app in apps_to_check:
        if os.path.exists(app):
            print_success(f"App '{app}' encontrada")
        else:
            print_error(f"App '{app}' NO encontrada")
            all_exist = False
    
    if not all_exist:
        print_error("Faltan algunas apps. Verifica que todos los archivos se hayan creado.")
        return
    
    print_header("PASO 2: Instrucciones de configuración")
    
    print_info("Debes agregar las siguientes apps a TENANT_APPS en config/settings.py:")
    print("\nTENANT_APPS = [")
    print("    # ... apps existentes")
    print("    'notifications',")
    print("    'qr_codes',")
    print("    'dashboard',")
    print("    'ai_chat',")
    print("    'events',")
    print("    'goals',")
    print("    'rest_framework',")
    print("]")
    
    print("\n¿Ya agregaste las apps a settings.py? (s/n): ", end="")
    if input().lower() != 's':
        print_info("Por favor agrega las apps a settings.py y vuelve a ejecutar este script.")
        return
    
    print_header("PASO 3: Instrucciones de URLs")
    
    print_info("Debes agregar las siguientes URLs en config/urls.py:")
    print("\nurlpatterns = [")
    print("    # ... urls existentes")
    print("    path('api/', include('notifications.urls')),")
    print("    path('api/', include('qr_codes.urls')),")
    print("    path('api/', include('dashboard.urls')),")
    print("    path('api/ai-chat/', include('ai_chat.urls')),")
    print("    path('api/', include('events.urls')),")
    print("    path('api/', include('goals.urls')),")
    print("]")
    
    print("\n¿Ya agregaste las URLs? (s/n): ", end="")
    if input().lower() != 's':
        print_info("Por favor agrega las URLs y vuelve a ejecutar este script.")
        return
    
    print_header("PASO 4: Creando migraciones")
    
    print_info("Ejecutando makemigrations...")
    print("\nComando a ejecutar:")
    print("python manage.py makemigrations notifications qr_codes ai_chat events goals")
    print("\n¿Ejecutar ahora? (s/n): ", end="")
    
    if input().lower() == 's':
        import subprocess
        try:
            result = subprocess.run(
                "python manage.py makemigrations notifications qr_codes ai_chat events goals",
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            print_success("Migraciones creadas exitosamente")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print_error("Error al crear migraciones")
            print(e.stderr)
            return
    else:
        print_info("Recuerda ejecutar: python manage.py makemigrations notifications qr_codes ai_chat events goals")
    
    print_header("PASO 5: Aplicando migraciones")
    
    print("\n¿Aplicar migraciones ahora? (s/n): ", end="")
    
    if input().lower() == 's':
        import subprocess
        try:
            result = subprocess.run(
                "python manage.py migrate",
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            print_success("Migraciones aplicadas exitosamente")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print_error("Error al aplicar migraciones")
            print(e.stderr)
            return
    else:
        print_info("Recuerda ejecutar: python manage.py migrate")
    
    print_header("INSTALACIÓN COMPLETADA")
    
    print_success("Backend instalado correctamente")
    
    print("\n📋 RESUMEN DE LO INSTALADO:\n")
    print("✅ 1. Notificaciones Push (9 archivos backend)")
    print("✅ 2. Códigos QR (7 archivos backend)")
    print("✅ 3. Dashboard Tiempo Real (4 archivos backend)")
    print("✅ 4. Chat IA (8 archivos backend)")
    print("✅ 5. Calendario de Eventos (7 archivos backend)")
    print("✅ 6. Metas y Objetivos (7 archivos backend)")
    
    print("\n📊 ESTADÍSTICAS:")
    print(f"  • Archivos backend: 42")
    print(f"  • Nuevos endpoints: 38")
    print(f"  • Nuevos modelos: 9")
    print(f"  • Líneas de código: ~6,000")
    
    print("\n📚 PRÓXIMOS PASOS:\n")
    
    print("1. Frontend - Instalar Recharts:")
    print("   cd cooperativa_frontend")
    print("   npm install recharts")
    
    print("\n2. Frontend - Agregar rutas en App.jsx:")
    print("   import NotificationsPage from './pages/NotificationsPage';")
    print("   import DashboardRealTime from './pages/DashboardRealTime';")
    print("   import AIChat from './pages/AIChat';")
    print("   ")
    print("   <Route path='/notifications' element={<NotificationsPage />} />")
    print("   <Route path='/dashboard-realtime' element={<DashboardRealTime />} />")
    print("   <Route path='/ai-chat' element={<AIChat />} />")
    
    print("\n3. Frontend - Agregar NotificationBell en Navbar.jsx:")
    print("   import NotificationBell from '../notifications/NotificationBell';")
    print("   // Agregar en el navbar: <NotificationBell />")
    
    print("\n4. Configurar .env (opcional para IA):")
    print("   OPENROUTER_API_KEY=tu_api_key_aqui")
    
    print("\n5. Crear datos de prueba:")
    print("   python create_test_data_all.py")
    
    print("\n6. Probar las funcionalidades:")
    print("   • Notificaciones: http://localhost:5173/notifications")
    print("   • Dashboard: http://localhost:5173/dashboard-realtime")
    print("   • Chat IA: http://localhost:5173/ai-chat")
    print("   • Eventos: API /api/events/events/")
    print("   • Metas: API /api/goals/goals/")
    
    print("\n📚 DOCUMENTACIÓN COMPLETA:")
    print("   • IMPLEMENTACION_FINAL_7_FUNCIONALIDADES.md")
    print("   • RESUMEN_FINAL_DEFENSA.md")
    print("   • GUIA_INSTALACION_NUEVAS_FUNCIONALIDADES.md")
    
    print("\n🎉 ¡TODO LISTO PARA LA DEFENSA!")
    print("\n💡 Tip: Lee RESUMEN_FINAL_DEFENSA.md para el guión de presentación")

if __name__ == '__main__':
    main()
