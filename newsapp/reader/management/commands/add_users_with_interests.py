from django.core.management.base import BaseCommand
from accounts.models import User, Interest

class Command(BaseCommand):
    help = 'Create default users with predefined interests'

    def handle(self, *args, **options):
        default_users = [
            {
                'full_name': 'user3',
                'password': 'User3pass!',
                'email': 'user3@example.com',
                'interests': ['Technology', 'Entertainment', 'Politics']
            },
            {
                'full_name': 'user4',
                'password': 'User4pass!',
                'email': 'user4@example.com',
                'interests': ['Technology', 'Food']
            },
            # Add more users here if needed
        ]

        for user_data in default_users:
            full_name = user_data['full_name']
            password = user_data['password']
            email = user_data['email']
            interests = user_data['interests']

            if not User.objects.filter(email=email, full_name=full_name).exists():
                user = User.objects.create_user(email=email, full_name=full_name, password=password)
                for interest_name in interests:
                    interest, created = Interest.objects.get_or_create(name=interest_name)
                    user.interests.add(interest)
                self.stdout.write(self.style.SUCCESS(f'Successfully created user: {full_name} with interests: {interests}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'User already exists: {full_name}'))
