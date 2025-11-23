import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from partners.models import Partner, Community
from users.models import User

# Obtener o crear una comunidad
community, created = Community.objects.get_or_create(
    name='Comunidad San José',
    defaults={'description': 'Comunidad de prueba', 'is_active': True}
)

if created:
    print(f'✅ Comunidad creada: {community.name}')
else:
    print(f'✅ Comunidad existente: {community.name}')

# Obtener usuario admin
admin_user = User.objects.get(username='admin')

# Intentar crear un socio
try:
    partner = Partner.objects.create(
        ci='1234567',
        first_name='Juan',
        last_name='Pérez',
        phone='70123456',
        email='juan@test.com',
        address='Calle 123',
        community=community,
        created_by=admin_user
    )
    print(f'✅ Socio creado exitosamente: {partner.full_name}')
    print(f'   - CI: {partner.ci}')
    print(f'   - Teléfono: {partner.phone}')
    print(f'   - Comunidad: {partner.community.name}')
except Exception as e:
    print(f'❌ Error al crear socio: {e}')
    import traceback
    traceback.print_exc()
