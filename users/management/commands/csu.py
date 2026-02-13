# users/management/commands/csu.py
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Проверяем, существует ли уже пользователь
        if not User.objects.filter(email='admin@example.com').exists():
            user = User.objects.create(
                email='admin@example.com',
                username='admin_user',
                phone_number='+79999999999',  # Добавить
                country='Россия',  # Добавить
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            user.set_password('123qwe')
            user.save()
            self.stdout.write(self.style.SUCCESS('Суперпользователь создан'))
        else:
            self.stdout.write(self.style.WARNING('Суперпользователь уже существует'))