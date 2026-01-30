from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
import random


# Optional: redirect old URLs safely
def category_redirect(request, slug):
    return redirect(f"/products/category/all/?category={slug}")


def shop_all(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    active_category = request.GET.get("category")

    if active_category:
        products = products.filter(category__slug=active_category)

    return render(request, "products/shop_all.html", {
        "categories": categories,
        "products": products,
        "active_category": active_category,
        "active_nav": "shop",
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # 🔥 Fake but realistic interest count (NO DB HIT)
    interest_count = (product.id % 5) + random.randint(6, 18)

    return render(request, "product_detail.html", {
        "product": product,
        "interest_count": interest_count,
    })
