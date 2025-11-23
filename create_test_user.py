import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

# Crear o actualizar usuario de prueba
username = 'admin'
password = 'admin123'

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        'email': 'admin@gmail.com',
        'first_name': 'Admin',
        'last_name': 'Sistema',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    }
)

if created:
    user.set_password(password)
    user.save()
    print(f'✅ Usuario creado: {username} / {password}')
else:
    user.set_password(password)
    user.is_active = True
    user.save()
    print(f'✅ Usuario actualizado: {username} / {password}')

print(f'Email: {user.email}')
print(f'Activo: {user.is_active}')
print(f'Staff: {user.is_staff}')
