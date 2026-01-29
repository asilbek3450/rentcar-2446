from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Superuser yaratish (asilbek/1234)'

    def handle(self, *args, **options):
        username = 'asilbek'
        password = '1234'
        email = 'asilbek@rentcar.uz'
        
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser yangilandi: {username}'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser yaratildi: {username} / {password}'))
