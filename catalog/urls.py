from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('home/', views.home, name='home'),  # главная: /
    path('contacts/', views.contacts, name='contacts'),  # контакты: /contacts/
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # товар: /product/1/
]