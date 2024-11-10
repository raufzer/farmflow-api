from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.account.models import Profile 

class Command(BaseCommand):
    help = 'Creates profiles for existing users without them'

    def handle(self, *args, **options):
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Profile created for user {user.username}'))
