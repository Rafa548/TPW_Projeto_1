from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create default users'

    def handle(self, *args, **options):
        default_users = [
            {'full_name': 'user1', 'password': 'User1pass!', 'email': 'user1@example.com'},
            {'full_name': 'user2', 'password': 'User2pass!', 'email': 'user2@example.com'},
            # Add more users here if needed
        ]

        for user_data in default_users:
            full_name = user_data['full_name']
            password = user_data['password']
            email = user_data['email']

            if not User.objects.filter(email=email, full_name=full_name).exists():
                User.objects.create_user(email=email, full_name=full_name, password=password)
                self.stdout.write(self.style.SUCCESS(f'Successfully created user: {full_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'User already exists: {full_name}'))
