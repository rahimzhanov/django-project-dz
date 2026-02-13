# catalog/management/commands/clear_cache.py использование "python manage.py clear_cache"
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Очистка всего кеша'

    def handle(self, *args, **options):
        cache.clear()
        self.stdout.write(
            self.style.SUCCESS('Кеш успешно очищен!')
        )