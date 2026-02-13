# catalog/services.py
from django.core.cache import cache
from django.conf import settings
from .models import Product, Category


def get_products_by_category(category_id):
    """
    Сервисная функция для получения всех продуктов в указанной категории
    """
    # Пытаемся получить данные из кеша
    cache_key = f'products_category_{category_id}'
    products = cache.get(cache_key)

    if not products:
        # Если в кеше нет, получаем из базы
        products = Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related('category', 'owner')

        # Сохраняем в кеш на 15 минут
        cache.set(cache_key, products, timeout=60 * 15)

    return products


def get_category_name(category_id):
    """
    Получает название категории по ID
    """
    cache_key = f'category_name_{category_id}'
    category_name = cache.get(cache_key)

    if not category_name:
        try:
            category = Category.objects.get(id=category_id)
            category_name = category.name
            cache.set(cache_key, category_name, timeout=60 * 15)
        except Category.DoesNotExist:
            category_name = 'Неизвестная категория'

    return category_name