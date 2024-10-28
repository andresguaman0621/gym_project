from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Lists all registered users'

    def handle(self, *args, **options):
        all_users = User.objects.all()
        for user in all_users:
            self.stdout.write(f'{user.username} - {user.email} - {user.date_joined}')
