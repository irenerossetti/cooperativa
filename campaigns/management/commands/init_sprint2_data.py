from django.core.management.base import BaseCommand
from farm_activities.models import ActivityType
from inventory.models import InventoryCategory


class Command(BaseCommand):
    help = 'Inicializa datos básicos del Sprint 2'

    def handle(self, *args, **options):
        # Crear tipos de labor
        activity_types = [
            {'name': ActivityType.SOWING, 'description': 'Actividades de siembra'},
            {'name': ActivityType.IRRIGATION, 'description': 'Actividades de riego'},
            {'name': ActivityType.FERTILIZATION, 'description': 'Aplicación de fertilizantes'},
            {'name': ActivityType.PEST_CONTROL, 'description': 'Control de plagas y enfermedades'},
            {'name': ActivityType.HARVEST, 'description': 'Actividades de cosecha'},
            {'name': ActivityType.OTHER, 'description': 'Otras actividades agrícolas'},
        ]

        for activity_data in activity_types:
            activity, created = ActivityType.objects.get_or_create(
                name=activity_data['name'],
                defaults={'description': activity_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Tipo de labor "{activity.get_name_display()}" creado'))
            else:
                self.stdout.write(self.style.WARNING(f'Tipo de labor "{activity.get_name_display()}" ya existe'))

        # Crear categorías de inventario
        categories = [
            {'name': InventoryCategory.SEED, 'description': 'Semillas y material de siembra'},
            {'name': InventoryCategory.PESTICIDE, 'description': 'Pesticidas y productos fitosanitarios'},
            {'name': InventoryCategory.FERTILIZER, 'description': 'Fertilizantes y abonos'},
            {'name': InventoryCategory.TOOL, 'description': 'Herramientas y equipos'},
            {'name': InventoryCategory.OTHER, 'description': 'Otros insumos'},
        ]

        for category_data in categories:
            category, created = InventoryCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoría "{category.get_name_display()}" creada'))
            else:
                self.stdout.write(self.style.WARNING(f'Categoría "{category.get_name_display()}" ya existe'))

        self.stdout.write(self.style.SUCCESS('\n✅ Inicialización de datos del Sprint 2 completada'))
