# catalog/management/commands/create_groups.py
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создание групп и назначение прав'

    def handle(self, *args, **options):
        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем или создаем разрешения
        can_unpublish, created = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            content_type=content_type,
            defaults={'name': 'Может отменять публикацию продукта'}
        )

        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Назначаем права группе
        # 1. Право отмены публикации
        moderator_group.permissions.add(can_unpublish)

        # 2. Право удаления любого продукта (стандартное разрешение Django)
        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )
        moderator_group.permissions.add(delete_permission)

        # 3. Право изменения любого продукта
        change_permission = Permission.objects.get(
            codename='change_product',
            content_type=content_type
        )
        moderator_group.permissions.add(change_permission)

        self.stdout.write(
            self.style.SUCCESS(
                f'Группа "Модератор продуктов" создана. Права назначены: '
                f'{moderator_group.permissions.count()} разрешений'
            )
        )