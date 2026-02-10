# catalog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from catalog.models import Product, Category
from catalog.forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Показываем только опубликованные продукты на главной
        return Product.objects.filter(is_published=True)[:6]


class ContactsView(View):
    template_name = 'catalog/contacts.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо {name}! сообщение получено.')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_form_kwargs(self):
        """Передаем пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Продукт создается, владелец автоматически устанавливается в форме
        return super().form_valid(form)


class IsOwnerOrModeratorMixin:
    """Миксин для проверки, что пользователь - владелец или модератор"""

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        # Проверяем, является ли пользователь владельцем
        is_owner = product.owner == user

        # Проверяем, является ли пользователь модератором
        is_moderator = user.has_perm('catalog.delete_product') or user.groups.filter(
            name='Модератор продуктов').exists()

        # Разрешаем доступ владельцу или модератору
        return is_owner or is_moderator

    def handle_no_permission(self):
        """Обработка отсутствия прав"""
        return HttpResponseForbidden("У вас нет прав для выполнения этого действия")


class ProductUpdateView(LoginRequiredMixin, IsOwnerOrModeratorMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        """Передаем пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """Добавляем информацию о правах в контекст"""
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        user = self.request.user

        context['is_owner'] = product.owner == user
        context['is_moderator'] = user.groups.filter(name='Модератор продуктов').exists() or user.has_perm(
            'catalog.delete_product')

        return context


class ProductDeleteView(LoginRequiredMixin, IsOwnerOrModeratorMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление продукта'

        product = self.get_object()
        user = self.request.user

        context['is_owner'] = product.owner == user
        context['is_moderator'] = user.groups.filter(name='Модератор продуктов').exists() or user.has_perm(
            'catalog.delete_product')

        return context

    def delete(self, request, *args, **kwargs):
        product = self.get_object()

        # Логирование удаления (можно добавить в будущем)
        print(f"Продукт {product.name} удален пользователем {request.user.email}")

        return super().delete(request, *args, **kwargs)


# Дополнительный view для отмены публикации (для модераторов)
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('catalog.can_unpublish_product', raise_exception=True), name='dispatch')
class ProductUnpublishView(View):
    """View для отмены публикации продукта (только для модераторов)"""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Отменяем публикацию
        product.is_published = False
        product.status = Product.Status.NOT_PUBLISHED
        product.save()

        return redirect('catalog:product_detail', pk=product.pk)