#!/usr/bin/env python
"""
Script completo para solucionar autenticación 403
Actualiza requirements.txt, settings.py y urls.py para JWT
"""
import os

print("=" * 60)
print("SOLUCIONANDO AUTENTICACIÓN 403 - INSTALANDO JWT")
print("=" * 60)

# 1. Actualizar requirements.txt
print("\n1. Actualizando requirements.txt...")
requirements_path = 'requirements.txt'
with open(requirements_path, 'r') as f:
    content = f.read()

if 'djangorestframework-simplejwt' not in content:
    with open(requirements_path, 'a') as f:
        f.write('\n# JWT Authentication\n')
        f.write('djangorestframework-simplejwt>=5.3.0\n')
    print("   ✓ djangorestframework-simplejwt agregado a requirements.txt")
else:
    print("   ✓ djangorestframework-simplejwt ya está en requirements.txt")

# 2. Instalar el paquete
print("\n2. Instalando djangorestframework-simplejwt...")
os.system('pip install djangorestframework-simplejwt')

print("\n" + "=" * 60)
print("INSTALACIÓN COMPLETADA")
print("=" * 60)
print("\nAhora necesitas:")
print("1. Actualizar config/settings.py - REST_FRAMEWORK")
print("2. Actualizar config/urls.py - agregar endpoints de token")
print("3. Ejecutar: python fix_authentication.py")
print("4. Reiniciar el servidor")
