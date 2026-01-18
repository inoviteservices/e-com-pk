from django.shortcuts import render
from pages.models import HomePage
from products.models import Category, Product


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)[:8]

    home_page = HomePage.objects.first()

    slides = []

    if home_page:
        slides = home_page.hero_slides.all()

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "slides": slides,
    })

def terms_of_service(request):
    return render(request, "pages/terms-of-service.html")

def shipping_policy(request):
    return render(request, "pages/shipping-policy.html")

def return_policy(request):
    return render(request, "pages/return-policy.html")

def privacy_policy(request):
    return render(request, "pages/privacy-policy.html")
