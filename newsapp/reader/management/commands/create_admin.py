from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create a default admin user'

    def handle(self, *args, **options):
        full_name = 'admin'
        password = 'admin' 
        email = 'admin@default.com'  

        if not User.objects.filter(email=email,full_name=full_name).exists():
            User.objects.create_superuser(email,full_name,password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created default admin user: {full_name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Default admin user already exists: {full_name}'))
