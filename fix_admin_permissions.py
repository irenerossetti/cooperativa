import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User, Role

# Crear o obtener rol de administrador
admin_role, created = Role.objects.get_or_create(
    name='ADMIN',
    defaults={
        'description': 'Administrador del sistema',
        'permissions': {'all': True},
        'is_active': True,
    }
)

if created:
    print(f'✅ Rol ADMIN creado')
else:
    print(f'✅ Rol ADMIN ya existe')

# Asignar rol al usuario admin
try:
    admin_user = User.objects.get(username='admin')
    admin_user.role = admin_role
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print(f'✅ Usuario admin actualizado con rol ADMIN')
    print(f'   - Username: {admin_user.username}')
    print(f'   - Email: {admin_user.email}')
    print(f'   - Rol: {admin_user.role.name if admin_user.role else "Sin rol"}')
    print(f'   - Staff: {admin_user.is_staff}')
    print(f'   - Superuser: {admin_user.is_superuser}')
except User.DoesNotExist:
    print('❌ Usuario admin no encontrado')
