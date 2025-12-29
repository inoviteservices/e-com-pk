from django.shortcuts import render, get_object_or_404
from .models import HeroSlide, Product, Category

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)[:8]

    DEFAULT_SLIDES = [
        "/static/images/hero1.png",
        "/static/images/hero2.png",
        "/static/images/hero3.png",
    ]

    db_slides = list(
        HeroSlide.objects
        .order_by("created_at")[:5]
    )

    final_slides = []

    # Add DB slides
    for slide in db_slides:
        final_slides.append(slide.image.url)

    # Fill till minimum 3
    for default in DEFAULT_SLIDES:
        if len(final_slides) < 3:
            final_slides.append(default)

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "slides": final_slides,
    })


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
