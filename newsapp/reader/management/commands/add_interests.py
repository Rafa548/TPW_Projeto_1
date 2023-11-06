from django.core.management.base import BaseCommand
from accounts.models import Interest

class Command(BaseCommand):
    help = 'Add interests to the database'

    def handle(self, *args, **options):
        #Interests to be added
        interests_to_add = ['Technology', 'Sports', 'Movies']

        for interest_name in interests_to_add:
            Interest.objects.get_or_create(name=interest_name)

        self.stdout.write(self.style.SUCCESS('Interests added to the database.'))
