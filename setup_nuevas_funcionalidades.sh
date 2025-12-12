#!/bin/bash

echo "🚀 Configurando nuevas funcionalidades..."
echo ""

# Crear migraciones
echo "📝 Creando migraciones..."
python manage.py makemigrations notifications
python manage.py makemigrations qr_codes
python manage.py makemigrations ai_chat
python manage.py makemigrations events
python manage.py makemigrations goals
python manage.py makemigrations dashboard

echo ""
echo "✅ Migraciones creadas"
echo ""

# Aplicar migraciones
echo "📦 Aplicando migraciones..."
python manage.py migrate

echo ""
echo "✅ Migraciones aplicadas"
echo ""

# Verificar instalación
echo "🔍 Verificando instalación..."
python test_new_endpoints.py

echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📝 Próximos pasos:"
echo "   1. Ejecuta: python manage.py runserver"
echo "   2. Accede a: http://localhost:8000"
echo "   3. Prueba los nuevos endpoints"
echo ""
