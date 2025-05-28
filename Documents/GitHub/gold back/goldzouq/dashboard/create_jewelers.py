# management/commands/create_jewelers.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create jeweler users'

    def handle(self, *args, **options):
        jewelers_data = [
            {'username': 'jeweler1', 'password': 'password1', 'email': 'jeweler1@example.com'},
            {'username': 'jeweler2', 'password': 'password2', 'email': 'jeweler2@example.com'},
            # Add more jeweler data as needed
        ]

        for data in jewelers_data:
            username = data['username']
            password = data['password']
            email = data['email']
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password, email=email, is_jeweler=True)
                self.stdout.write(self.style.SUCCESS(f'Created jeweler user: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} already exists'))
