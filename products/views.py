from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)

    return render(request, 'category.html', {
        'category': category,
        'products': products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    return render(request, 'product_detail.html', {
        'product': product
    })
