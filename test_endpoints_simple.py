"""
Script simple para probar los endpoints de las nuevas funcionalidades
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver

print("🔍 Verificando URLs registradas...\n")

resolver = get_resolver()
url_patterns = resolver.url_patterns

# URLs que buscamos
urls_to_check = [
    'api/notifications/',
    'api/events/',
    'api/goals/',
    'api/dashboard/',
    'api/ai-chat/',
    'api/qr-codes/',
]

print("✅ URLs en config/urls.py:\n")
for pattern in url_patterns:
    pattern_str = str(pattern.pattern)
    if any(url in pattern_str for url in urls_to_check):
        print(f"   ✓ {pattern_str}")

print("\n" + "="*60)
print("🧪 Probando importación de módulos...")
print("="*60 + "\n")

modules_to_test = [
    ('notifications.models', 'Notification'),
    ('events.models', 'Event'),
    ('goals.models', 'Goal'),
    ('ai_chat.models', 'ChatConversation'),
    ('qr_codes.models', 'QRCode'),
]

all_ok = True
for module_name, class_name in modules_to_test:
    try:
        module = __import__(module_name, fromlist=[class_name])
        cls = getattr(module, class_name)
        print(f"✅ {module_name}.{class_name} - OK")
    except Exception as e:
        print(f"❌ {module_name}.{class_name} - ERROR: {e}")
        all_ok = False

print("\n" + "="*60)
if all_ok:
    print("✅ Todos los módulos se importaron correctamente")
else:
    print("⚠️  Algunos módulos tienen errores")
print("="*60)
