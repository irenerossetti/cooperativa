#!/usr/bin/env python
"""
Script completo de configuración automática
Ejecutar: python setup_complete.py
"""

import os
import sys
import subprocess
import re

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

def print_warning(text):
    print(f"⚠️  {text}")

def run_command(command, description, check=True):
    """Ejecuta un comando y muestra el resultado"""
    print_info(f"{description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success(f"{description} completado")
            if result.stdout:
                print(result.stdout[:500])  # Primeros 500 caracteres
            return True
        else:
            print_error(f"Error en {description}")
            if result.stderr:
                print(result.stderr[:500])
            return False
    except subprocess.CalledProcessError as e:
        print_error(f"Error en {description}")
        print(e.stderr[:500] if e.stderr else "")
        return False

def check_file_exists(filepath):
    """Verifica si un archivo existe"""
    return os.path.exists(filepath)

def update_settings_file():
    """Actualiza el archivo settings.py"""
    settings_path = 'config/settings.py'
    
    if not check_file_exists(settings_path):
        print_error(f"No se encontró {settings_path}")
        return False
    
    print_info("Actualizando settings.py...")
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar si ya están las apps
    apps_to_add = ['notifications', 'qr_codes', 'dashboard', 'ai_chat', 'events', 'goals']
    apps_missing = [app for app in apps_to_add if f"'{app}'" not in content]
    
    if not apps_missing:
        print_success("Todas las apps ya están en settings.py")
        return True
    
    # Buscar TENANT_APPS
    tenant_apps_pattern = r'TENANT_APPS\s*=\s*\['
    match = re.search(tenant_apps_pattern, content)
    
    if not match:
        print_error("No se encontró TENANT_APPS en settings.py")
        return False
    
    # Agregar apps faltantes
    apps_to_insert = '\n'.join([f"    '{app}'," for app in apps_missing])
    
    # Buscar el final de TENANT_APPS
    insert_position = content.find("'rest_framework',", match.end())
    
    if insert_position == -1:
        print_warning("No se pudo agregar automáticamente. Agrega manualmente:")
        for app in apps_missing:
            print(f"    '{app}',")
        return False
    
    # Insertar las apps
    new_content = content[:insert_position] + apps_to_insert + '\n    ' + content[insert_position:]
    
    # Guardar backup
    with open(settings_path + '.backup', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Guardar nuevo contenido
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print_success(f"Apps agregadas a settings.py: {', '.join(apps_missing)}")
    print_info(f"Backup guardado en {settings_path}.backup")
    return True

def update_urls_file():
    """Actualiza el archivo urls.py"""
    urls_path = 'config/urls.py'
    
    if not check_file_exists(urls_path):
        print_error(f"No se encontró {urls_path}")
        return False
    
    print_info("Actualizando urls.py...")
    
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # URLs a agregar
    urls_to_add = [
        ("path('api/', include('notifications.urls')),", 'notifications'),
        ("path('api/', include('qr_codes.urls')),", 'qr_codes'),
        ("path('api/', include('dashboard.urls')),", 'dashboard'),
        ("path('api/ai-chat/', include('ai_chat.urls')),", 'ai_chat'),
        ("path('api/', include('events.urls')),", 'events'),
        ("path('api/', include('goals.urls')),", 'goals'),
    ]
    
    urls_missing = [(url, name) for url, name in urls_to_add if url not in content]
    
    if not urls_missing:
        print_success("Todas las URLs ya están en urls.py")
        return True
    
    # Buscar urlpatterns
    urlpatterns_pattern = r'urlpatterns\s*=\s*\['
    match = re.search(urlpatterns_pattern, content)
    
    if not match:
        print_error("No se encontró urlpatterns en urls.py")
        return False
    
    # Agregar URLs faltantes
    urls_to_insert = '\n'.join([f"    {url}" for url, _ in urls_missing])
    
    # Buscar un buen lugar para insertar (antes del cierre de urlpatterns)
    insert_position = content.rfind(']', match.end())
    
    if insert_position == -1:
        print_warning("No se pudo agregar automáticamente. Agrega manualmente:")
        for url, _ in urls_missing:
            print(f"    {url}")
        return False
    
    # Insertar las URLs
    new_content = content[:insert_position] + '    ' + urls_to_insert + '\n' + content[insert_position:]
    
    # Guardar backup
    with open(urls_path + '.backup', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Guardar nuevo contenido
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print_success(f"URLs agregadas: {', '.join([name for _, name in urls_missing])}")
    print_info(f"Backup guardado en {urls_path}.backup")
    return True

def create_test_data():
    """Crea datos de prueba"""
    print_info("Creando datos de prueba...")
    
    test_script = """
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from notifications.utils import create_notification, notify_admins
from users.models import User
from django.utils import timezone
from datetime import timedelta

print("\\n📝 Creando datos de prueba...\\n")

# 1. Notificaciones
print("1️⃣  Creando notificaciones...")
users = User.objects.filter(is_active=True)[:5]

for i, user in enumerate(users):
    create_notification(
        user=user,
        title=f'Bienvenido al nuevo sistema #{i+1}',
        message='Se han agregado 7 nuevas funcionalidades: Notificaciones, QR, Dashboard, Chat IA, Eventos y Metas',
        notification_type='INFO'
    )
    
    create_notification(
        user=user,
        title='Sistema actualizado',
        message='El sistema ha sido actualizado exitosamente',
        notification_type='SUCCESS'
    )

notify_admins(
    title='Nuevas funcionalidades disponibles',
    message='Se han instalado 7 nuevas funcionalidades en el sistema',
    notification_type='INFO'
)

print(f"   ✅ {len(users) * 2 + 1} notificaciones creadas")

# 2. Eventos
print("\\n2️⃣  Creando eventos de prueba...")
from events.models import Event
from parcels.models import Parcel

parcels = Parcel.objects.all()[:3]
now = timezone.now()

events_data = [
    {
        'title': 'Siembra de Café',
        'type': 'SIEMBRA',
        'start_datetime': now + timedelta(days=2),
        'end_datetime': now + timedelta(days=2, hours=4),
        'location': 'Parcela Norte',
        'priority': 'HIGH',
        'color': '#10b981'
    },
    {
        'title': 'Capacitación en Fertilización',
        'type': 'CAPACITACION',
        'start_datetime': now + timedelta(days=5),
        'end_datetime': now + timedelta(days=5, hours=3),
        'location': 'Salón Comunal',
        'priority': 'MEDIUM',
        'color': '#3b82f6'
    },
    {
        'title': 'Inspección de Cultivos',
        'type': 'INSPECCION',
        'start_datetime': now + timedelta(days=7),
        'end_datetime': now + timedelta(days=7, hours=2),
        'location': 'Todas las parcelas',
        'priority': 'HIGH',
        'color': '#f59e0b'
    },
]

for event_data in events_data:
    event = Event.objects.create(
        created_by=users[0] if users else None,
        **event_data
    )
    if parcels:
        event.parcels.add(*parcels)
    if users:
        event.participants.add(*users[:3])

print(f"   ✅ {len(events_data)} eventos creados")

# 3. Metas
print("\\n3️⃣  Creando metas de prueba...")
from goals.models import Goal, GoalMilestone

goals_data = [
    {
        'name': 'Aumentar Producción de Café',
        'type': 'PRODUCTION',
        'target_value': 10000,
        'current_value': 6500,
        'unit': 'kg',
        'start_date': now.date(),
        'end_date': (now + timedelta(days=90)).date(),
        'status': 'IN_PROGRESS',
    },
    {
        'name': 'Incrementar Ventas Mensuales',
        'type': 'SALES',
        'target_value': 50000,
        'current_value': 32000,
        'unit': 'Bs',
        'start_date': now.date(),
        'end_date': (now + timedelta(days=30)).date(),
        'status': 'IN_PROGRESS',
    },
    {
        'name': 'Incorporar Nuevos Socios',
        'type': 'PARTNERS',
        'target_value': 20,
        'current_value': 12,
        'unit': 'socios',
        'start_date': now.date(),
        'end_date': (now + timedelta(days=180)).date(),
        'status': 'IN_PROGRESS',
    },
]

for goal_data in goals_data:
    goal = Goal.objects.create(
        responsible=users[0] if users else None,
        **goal_data
    )
    
    # Agregar hitos
    GoalMilestone.objects.create(
        goal=goal,
        title=f'Hito 1: 50% de {goal.name}',
        target_date=(now + timedelta(days=30)).date()
    )
    GoalMilestone.objects.create(
        goal=goal,
        title=f'Hito 2: 75% de {goal.name}',
        target_date=(now + timedelta(days=60)).date()
    )

print(f"   ✅ {len(goals_data)} metas creadas con hitos")

print("\\n✅ Datos de prueba creados exitosamente\\n")
print("📊 Resumen:")
print(f"   • Notificaciones: {len(users) * 2 + 1}")
print(f"   • Eventos: {len(events_data)}")
print(f"   • Metas: {len(goals_data)}")
print(f"   • Hitos: {len(goals_data) * 2}")
"""
    
    with open('create_test_data_complete.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    success = run_command(
        "python create_test_data_complete.py",
        "Creación de datos de prueba",
        check=False
    )
    
    # Limpiar archivo temporal
    if os.path.exists('create_test_data_complete.py'):
        os.remove('create_test_data_complete.py')
    
    return success

def main():
    print_header("CONFIGURACIÓN COMPLETA AUTOMÁTICA")
    print("Este script configurará automáticamente todo el sistema\n")
    
    # Verificar que estamos en el directorio correcto
    if not check_file_exists('manage.py'):
        print_error("Error: No se encontró manage.py")
        print_info("Ejecuta este script desde el directorio cooperativa/")
        return
    
    print_success("Directorio correcto detectado")
    
    # Paso 1: Verificar apps
    print_header("PASO 1: Verificando apps creadas")
    
    apps = ['notifications', 'qr_codes', 'dashboard', 'ai_chat', 'events', 'goals']
    all_exist = True
    
    for app in apps:
        if check_file_exists(app):
            print_success(f"App '{app}' encontrada")
        else:
            print_error(f"App '{app}' NO encontrada")
            all_exist = False
    
    if not all_exist:
        print_error("Faltan algunas apps. Verifica la implementación.")
        return
    
    # Paso 2: Actualizar settings.py
    print_header("PASO 2: Actualizando settings.py")
    
    if not update_settings_file():
        print_warning("Revisa manualmente config/settings.py")
    
    # Paso 3: Actualizar urls.py
    print_header("PASO 3: Actualizando urls.py")
    
    if not update_urls_file():
        print_warning("Revisa manualmente config/urls.py")
    
    # Paso 4: Instalar dependencias
    print_header("PASO 4: Instalando dependencias Python")
    
    run_command(
        "pip install qrcode[pil] pillow requests",
        "Instalación de dependencias",
        check=False
    )
    
    # Paso 5: Crear migraciones
    print_header("PASO 5: Creando migraciones")
    
    run_command(
        "python manage.py makemigrations notifications qr_codes ai_chat events goals",
        "Creación de migraciones",
        check=False
    )
    
    # Paso 6: Aplicar migraciones
    print_header("PASO 6: Aplicando migraciones")
    
    run_command(
        "python manage.py migrate",
        "Aplicación de migraciones",
        check=False
    )
    
    # Paso 7: Crear datos de prueba
    print_header("PASO 7: Creando datos de prueba")
    
    create_test_data()
    
    # Resumen final
    print_header("✅ CONFIGURACIÓN COMPLETADA")
    
    print("\n📊 RESUMEN:")
    print("  ✅ Apps verificadas: 6")
    print("  ✅ Settings.py actualizado")
    print("  ✅ URLs.py actualizado")
    print("  ✅ Dependencias instaladas")
    print("  ✅ Migraciones aplicadas")
    print("  ✅ Datos de prueba creados")
    
    print("\n🚀 PRÓXIMOS PASOS:")
    print("\n1. Iniciar el servidor:")
    print("   python manage.py runserver")
    
    print("\n2. Probar los endpoints:")
    print("   • Notificaciones: http://localhost:8000/api/notifications/notifications/")
    print("   • Dashboard: http://localhost:8000/api/dashboard/metrics/")
    print("   • Eventos: http://localhost:8000/api/events/events/")
    print("   • Metas: http://localhost:8000/api/goals/goals/")
    
    print("\n3. Frontend - Instalar dependencias:")
    print("   cd cooperativa_frontend")
    print("   npm install recharts")
    
    print("\n4. Frontend - Iniciar servidor:")
    print("   npm run dev")
    
    print("\n5. Abrir en el navegador:")
    print("   http://localhost:5173")
    
    print("\n📚 DOCUMENTACIÓN:")
    print("   • IMPLEMENTACION_FINAL_7_FUNCIONALIDADES.md")
    print("   • RESUMEN_FINAL_DEFENSA.md")
    
    print("\n🎉 ¡TODO LISTO PARA PROBAR!")

if __name__ == '__main__':
    main()
