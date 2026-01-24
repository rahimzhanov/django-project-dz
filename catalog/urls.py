from django.urls import path
from .views import HomeView, ContactsView, ProductDetailView

app_name = 'catalog'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),  # главная: /
    path('contacts/', ContactsView.as_view(), name='contacts'),  # контакты: /contacts/
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # товар: /product/1/
]