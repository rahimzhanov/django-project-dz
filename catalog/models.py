# catalog/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Product(models.Model):
    # Статусы публикации
    class Status(models.TextChoices):
        PUBLISHED = 'published', 'Опубликован'
        NOT_PUBLISHED = 'not_published', 'Не опубликован'
        MODERATION = 'moderation', 'На модерации'

    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Новые поля для заданий
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован',
        help_text='Отметьте, если товар готов к публикации'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_PUBLISHED,
        verbose_name='Статус публикации'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец',
        related_name='products'
    )

    def __str__(self):
        return f'{self.name} {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
            ('can_change_product_description', 'Может изменять описание продукта'),
            ('can_change_product_category', 'Может изменять категорию продукта'),
        ]