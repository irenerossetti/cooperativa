"""
Script para verificar la conexión a la base de datos
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from users.models import User, Role
from partners.models import Partner, Community
from parcels.models import Parcel, SoilType, Crop
from audit.models import AuditLog

def test_connection():
    print("🔍 Verificando conexión a la base de datos...\n")
    
    try:
        # Test 1: Verificar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Conexión exitosa a PostgreSQL")
            print(f"   Versión: {version[0]}\n")
        
        # Test 2: Verificar tablas
        print("📊 Verificando tablas:")
        tables = connection.introspection.table_names()
        print(f"   Total de tablas: {len(tables)}")
        print(f"   Tablas principales: {[t for t in tables if not t.startswith('django_') and not t.startswith('auth_')]}\n")
        
        # Test 3: Contar registros
        print("📈 Contando registros:")
        print(f"   Usuarios: {User.objects.count()}")
        print(f"   Roles: {Role.objects.count()}")
        print(f"   Comunidades: {Community.objects.count()}")
        print(f"   Socios: {Partner.objects.count()}")
        print(f"   Tipos de Suelo: {SoilType.objects.count()}")
        print(f"   Cultivos: {Crop.objects.count()}")
        print(f"   Parcelas: {Parcel.objects.count()}")
        print(f"   Logs de Auditoría: {AuditLog.objects.count()}\n")
        
        # Test 4: Mostrar datos de ejemplo
        print("👤 Usuario administrador:")
        admin = User.objects.first()
        if admin:
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Rol: {admin.role.get_name_display() if admin.role else 'Sin rol'}\n")
        
        print("🎭 Roles disponibles:")
        for role in Role.objects.all():
            print(f"   - {role.get_name_display()}: {role.description}")
        print()
        
        print("🏘️ Comunidades:")
        for community in Community.objects.all():
            print(f"   - {community.name}: {community.partners.count()} socios")
        print()
        
        # Test 5: Verificar configuración de la BD
        print("⚙️ Configuración de la base de datos:")
        db_settings = connection.settings_dict
        print(f"   Engine: {db_settings['ENGINE']}")
        print(f"   Host: {db_settings['HOST']}")
        print(f"   Port: {db_settings['PORT']}")
        print(f"   Database: {db_settings['NAME']}")
        print(f"   User: {db_settings['USER']}\n")
        
        print("✅ ¡Todas las verificaciones pasaron exitosamente!")
        print("🎉 La base de datos está correctamente configurada y funcionando.\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos:")
        print(f"   {str(e)}\n")
        return False

if __name__ == "__main__":
    test_connection()
