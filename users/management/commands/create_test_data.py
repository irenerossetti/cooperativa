from django.core.management.base import BaseCommand
from users.models import User, Role
from partners.models import Partner, Community
from parcels.models import Parcel, SoilType, Crop


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema'

    def handle(self, *args, **options):
        # Crear comunidades
        communities = [
            Community.objects.get_or_create(name='Comunidad San José', defaults={'description': 'Comunidad del norte'})[0],
            Community.objects.get_or_create(name='Comunidad Santa María', defaults={'description': 'Comunidad del sur'})[0],
            Community.objects.get_or_create(name='Comunidad El Carmen', defaults={'description': 'Comunidad del este'})[0],
        ]
        self.stdout.write(self.style.SUCCESS(f'{len(communities)} comunidades creadas'))

        # Crear tipos de suelo
        soil_types = [
            SoilType.objects.get_or_create(name='Arcilloso', defaults={'description': 'Suelo con alta retención de agua'})[0],
            SoilType.objects.get_or_create(name='Arenoso', defaults={'description': 'Suelo con buen drenaje'})[0],
            SoilType.objects.get_or_create(name='Franco', defaults={'description': 'Suelo equilibrado'})[0],
        ]
        self.stdout.write(self.style.SUCCESS(f'{len(soil_types)} tipos de suelo creados'))

        # Crear cultivos
        crops = [
            Crop.objects.get_or_create(name='Café', defaults={'scientific_name': 'Coffea arabica'})[0],
            Crop.objects.get_or_create(name='Cacao', defaults={'scientific_name': 'Theobroma cacao'})[0],
            Crop.objects.get_or_create(name='Maíz', defaults={'scientific_name': 'Zea mays'})[0],
        ]
        self.stdout.write(self.style.SUCCESS(f'{len(crops)} cultivos creados'))

        # Crear usuario administrador
        admin_role = Role.objects.get(name=Role.ADMIN)
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@cooperativa.com',
                'first_name': 'Admin',
                'last_name': 'Sistema',
                'role': admin_role,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Usuario admin creado (username: admin, password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Usuario admin ya existe'))

        self.stdout.write(self.style.SUCCESS('Datos de prueba creados exitosamente'))
