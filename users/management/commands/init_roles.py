from django.core.management.base import BaseCommand
from users.models import Role


class Command(BaseCommand):
    help = 'Inicializa los roles del sistema'

    def handle(self, *args, **options):
        roles_data = [
            {
                'name': Role.ADMIN,
                'description': 'Administrador del sistema con acceso completo',
                'permissions': {
                    'users': {'create': True, 'read': True, 'update': True, 'delete': True},
                    'partners': {'create': True, 'read': True, 'update': True, 'delete': True},
                    'parcels': {'create': True, 'read': True, 'update': True, 'delete': True},
                    'audit': {'read': True},
                }
            },
            {
                'name': Role.PARTNER,
                'description': 'Socio de la cooperativa',
                'permissions': {
                    'partners': {'read': True},
                    'parcels': {'read': True},
                }
            },
            {
                'name': Role.OPERATOR,
                'description': 'Operador del sistema',
                'permissions': {
                    'partners': {'create': True, 'read': True, 'update': True},
                    'parcels': {'create': True, 'read': True, 'update': True},
                }
            },
        ]

        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'permissions': role_data['permissions']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Rol "{role.get_name_display()}" creado'))
            else:
                self.stdout.write(self.style.WARNING(f'Rol "{role.get_name_display()}" ya existe'))

        self.stdout.write(self.style.SUCCESS('Inicialización de roles completada'))
