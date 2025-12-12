"""
Script para probar el AI Chat
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ai_chat.ai_service import AIService
from django.contrib.auth import get_user_model

User = get_user_model()

print("🧪 Probando AI Chat Service...\n")

# Crear servicio
service = AIService()

print(f"✓ API Key configurada: {'Sí' if service.api_key else 'No'}")
print(f"✓ Modelo: {service.model}\n")

# Contexto de prueba simple
context = {
    'user': {'name': 'Test User', 'role': 'Admin'},
    'partners': {'total': 45, 'new_this_month': 3},
    'sales': {
        'today_count': 5,
        'today_amount': 1250.50,
        'this_month_count': 127,
        'this_month_amount': 45230.50
    },
    'inventory': {'total_items': 85, 'low_stock_items': 7}
}

print("📊 Contexto de prueba:")
print(f"   Socios: {context['partners']['total']}")
print(f"   Ventas hoy: {context['sales']['today_count']}")
print(f"   Items inventario: {context['inventory']['total_items']}\n")

# Probar mensaje del sistema
print("🔧 Probando construcción de mensaje del sistema...")
try:
    system_msg = service._build_system_message(context)
    print(f"✓ Mensaje del sistema creado ({len(system_msg)} caracteres)\n")
    print("Primeros 200 caracteres:")
    print(system_msg[:200] + "...\n")
except Exception as e:
    print(f"✗ Error: {e}\n")

# Probar respuesta fallback
print("🔧 Probando respuesta fallback...")
try:
    response = service._fallback_response("¿Cuántos socios tengo?", context)
    print(f"✓ Respuesta fallback generada\n")
    print("Respuesta:")
    print(response['content'][:200] + "...\n")
except Exception as e:
    print(f"✗ Error: {e}\n")

# Probar chat completo (usará fallback si API falla)
print("🔧 Probando chat completo...")
try:
    response = service.chat("¿Cuántos socios tengo?", context=context)
    print(f"✓ Chat completado")
    print(f"   Modelo usado: {response['model']}")
    print(f"   Tokens: {response['tokens_used']}\n")
    print("Respuesta:")
    print(response['content'][:300] + "...\n")
except Exception as e:
    print(f"✗ Error: {e}\n")
    import traceback
    traceback.print_exc()

print("="*60)
print("✅ Pruebas completadas")
