#!/usr/bin/env python
"""Script simple para probar OpenRouter"""
import sys
import os

# Agregar el path correcto para evitar conflictos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cargar .env
from dotenv import load_dotenv
load_dotenv()

# Importar urllib en lugar de requests para evitar conflictos
import urllib.request
import urllib.error
import json

def test_openrouter():
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
        return False
    
    # Preparar request
    print(f"\n2. Preparando request...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Cooperativa Chatbot Test"
    }
    
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "Eres un asistente de una cooperativa agrícola."},
            {"role": "user", "content": "Hola, necesito información sobre semillas de sésamo"}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    print(f"   📡 URL: {url}")
    print(f"   🤖 Modelo: {payload['model']}")
    
    # Hacer request
    print(f"\n3. Enviando request...")
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            ai_response = result['choices'][0]['message']['content']
            
            print(f"\n✅ ÉXITO! OpenRouter respondió:")
            print("=" * 60)
            print(ai_response)
            print("=" * 60)
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ ERROR HTTP: {e.code}")
        print(f"   Response: {e.read().decode('utf-8')[:500]}")
        return False
    except urllib.error.URLError as e:
        print(f"\n❌ ERROR de conexión: {e.reason}")
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
        print("🎉 OpenRouter funciona correctamente!")
    else:
        print("❌ OpenRouter no está funcionando")
    print("=" * 60)
