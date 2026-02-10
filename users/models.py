from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ImageField


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=15, verbose_name='Телефон', help_text='Введите номер телефона')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватар', help_text='Загрузите аватар')
    country = models.CharField(max_length=50, verbose_name='Страна', help_text='Введите страну')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email