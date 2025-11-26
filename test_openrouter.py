#!/usr/bin/env python
"""
Script para probar la conexión con OpenRouter
"""
import os
import sys
import django

# Importar requests antes de configurar Django para evitar conflictos
try:
    import requests as http_requests
except ImportError:
    print("❌ Error: requests no está instalado")
    print("Instala con: pip install requests")
    sys.exit(1)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dotenv import load_dotenv
load_dotenv()

def test_openrouter():
    """Prueba la conexión con OpenRouter"""
    print("=" * 60)
    print("🧪 PRUEBA DE OPENROUTER")
    print("=" * 60)
    
    # Verificar API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    print(f"\n1. Verificando API Key...")
    if api_key:
        print(f"   ✅ API Key encontrada: {api_key[:20]}...")
    else:
        print("   ❌ No se encontró OPENROUTER_API_KEY")
        print("   💡 Asegúrate de que esté en el archivo .env")
        return False
    
    # Preparar request
    print(f"\n2. Preparando request a OpenRouter...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Cooperativa Chatbot Test"
    }
    
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "Eres un asistente de una cooperativa agrícola."
            },
            {
                "role": "user",
                "content": "Hola, necesito información sobre semillas de sésamo"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    print(f"   📡 URL: {url}")
    print(f"   🤖 Modelo: {payload['model']}")
    print(f"   💬 Mensaje: {payload['messages'][1]['content']}")
    
    # Hacer request
    print(f"\n3. Enviando request...")
    try:
        response = http_requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"   📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data['choices'][0]['message']['content']
            
            print(f"\n✅ ÉXITO! OpenRouter respondió:")
            print("=" * 60)
            print(ai_response)
            print("=" * 60)
            return True
        else:
            print(f"\n❌ ERROR! OpenRouter respondió con error:")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except http_requests.exceptions.Timeout:
        print(f"\n❌ ERROR: Timeout - OpenRouter tardó más de 30 segundos")
        return False
    except http_requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: No se pudo conectar a OpenRouter")
        print(f"   Verifica tu conexión a internet")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_openrouter()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 PRUEBA EXITOSA - OpenRouter está funcionando")
        print("\n💡 Si el chatbot no usa IA, verifica:")
        print("   1. Que el servidor Django esté reiniciado")
        print("   2. Que no haya errores en la consola del servidor")
        print("   3. Que el archivo .env esté en Backend/")
    else:
        print("❌ PRUEBA FALLIDA - Revisa los errores arriba")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que OPENROUTER_API_KEY esté en .env")
        print("   2. Verifica tu conexión a internet")
        print("   3. Prueba con otra API key de OpenRouter")
    print("=" * 60)
