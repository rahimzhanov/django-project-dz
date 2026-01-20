from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.utils import timezone


class Command(BaseCommand):
    help = 'Добавляет тестовые продукты'

    def handle(self, *args, **options):
        # Удаляем все старые данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем категории
        cat1 = Category.objects.create(name="Электроника", description="Техника")
        cat2 = Category.objects.create(name="Одежда", description="Одежда")

        # Создаем продукты с текущим временем
        now = timezone.now()

        Product.objects.create(
            name="Телефон",
            description="Смартфон",
            category=cat1,
            price=10000,
            image="",
            created_at=now,
            updated_at=now
        )

        Product.objects.create(
            name="Ноутбук",
            description="Игровой",
            category=cat1,
            price=50000,
            image="",
            created_at=now,
            updated_at=now
        )

        Product.objects.create(
            name="Футболка",
            description="Хлопковая",
            category=cat2,
            price=1000,
            image="",
            created_at=now,
            updated_at=now
        )

        Product.objects.create(
            name="Джинсы",
            description="Синие",
            category=cat2,
            price=3000,
            image="",
            created_at=now,
            updated_at=now
        )

        print("✅ Тестовые данные созданы!")
        print(f"Категорий: {Category.objects.count()}")
        print(f"Продуктов: {Product.objects.count()}")