#!/usr/bin/env python
"""
Script para verificar que todos los nuevos endpoints estén funcionando
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver
from django.core.management import call_command

print("🔍 Verificando URLs de las nuevas funcionalidades...\n")

# URLs que deben existir
required_urls = [
    'api/notifications/notifications/',
    'api/events/events/',
    'api/goals/goals/',
    'api/dashboard/realtime/',
    'api/ai-chat/conversations/',
    'api/qr-codes/qr-codes/',
]

resolver = get_resolver()
all_patterns = []

def get_all_urls(urlpatterns, prefix=''):
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            get_all_urls(pattern.url_patterns, prefix + str(pattern.pattern))
        else:
            all_patterns.append(prefix + str(pattern.pattern))

get_all_urls(resolver.url_patterns)

print("✅ URLs Registradas:\n")
for url in required_urls:
    found = any(url in pattern for pattern in all_patterns)
    status = "✅" if found else "❌"
    print(f"{status} {url}")

print("\n" + "="*60)
print("📊 RESUMEN")
print("="*60)

found_count = sum(1 for url in required_urls if any(url in pattern for pattern in all_patterns))
total_count = len(required_urls)

print(f"\nURLs encontradas: {found_count}/{total_count}")

if found_count == total_count:
    print("\n🎉 ¡Todas las URLs están correctamente registradas!")
    print("\n📝 Próximos pasos:")
    print("   1. Ejecuta: python manage.py runserver")
    print("   2. Prueba los endpoints desde el frontend")
    print("   3. Verifica que el CRUD funcione correctamente")
else:
    print("\n⚠️  Faltan URLs por registrar")
    print("   Revisa el archivo config/urls.py")

print("\n" + "="*60)
