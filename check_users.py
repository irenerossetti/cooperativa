import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

print("=" * 60)
print("USUARIOS EN EL SISTEMA")
print("=" * 60)

users = User.objects.all()

for user in users:
    print(f"\n{'='*40}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Nombre: {user.first_name} {user.last_name}")
    print(f"Is Staff: {user.is_staff}")
    print(f"Is Superuser: {user.is_superuser}")
    print(f"Role: {getattr(user, 'role', 'N/A')}")
    print(f"Active: {user.is_active}")

print("\n" + "=" * 60)
print("CREDENCIALES PARA PROBAR:")
print("=" * 60)

# Buscar superusuario
superuser = User.objects.filter(is_superuser=True).first()
if superuser:
    print(f"\n✅ ADMINISTRADOR (Superusuario):")
    print(f"   Username: {superuser.username}")
    print(f"   Password: admin123 (por defecto)")
else:
    print("\n❌ No hay superusuario. Creando uno...")
    User.objects.create_superuser(
        username='admin',
        email='admin@cooperativa.com',
        password='admin123',
        first_name='Administrador',
        last_name='Sistema'
    )
    print("✅ Superusuario creado:")
    print("   Username: admin")
    print("   Password: admin123")

# Buscar staff
staff = User.objects.filter(is_staff=True, is_superuser=False).first()
if staff:
    print(f"\n✅ STAFF:")
    print(f"   Username: {staff.username}")
    print(f"   Password: (verificar en create_test_user.py)")

print("\n" + "=" * 60)
