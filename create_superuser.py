"""
Script para crear un super usuario para el panel de administración
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

def create_superuser():
    """Crea un super usuario si no existe"""
    username = 'superadmin'
    email = 'superadmin@agrocooperativa.com'
    password = 'admin123'  # Cambiar en producción
    
    if User.objects.filter(username=username).exists():
        print(f'❌ El usuario {username} ya existe')
        user = User.objects.get(username=username)
        print(f'✅ Usuario existente: {user.username} - Superuser: {user.is_superuser}')
        return
    
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Super',
        last_name='Admin'
    )
    
    print('✅ Super usuario creado exitosamente!')
    print(f'   Username: {username}')
    print(f'   Email: {email}')
    print(f'   Password: {password}')
    print(f'   Superuser: {user.is_superuser}')
    print(f'   Staff: {user.is_staff}')
    print()
    print('🔐 Accede al panel en: http://localhost:5173/super-admin')
    print('⚠️  IMPORTANTE: Cambia la contraseña en producción')

if __name__ == '__main__':
    create_superuser()
