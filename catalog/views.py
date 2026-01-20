from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from catalog.models import Product, Category

def home(request):
    products = Product.objects.all()[:6]  # Показываем только первые 6 товаров на главной
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо {name}! сообщение получено.')
    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})