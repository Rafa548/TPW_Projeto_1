from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Clean all records from the database'

    def handle(self, *args, **options):
        for model in apps.get_models():
            model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted all records from {model.__name__}'))
