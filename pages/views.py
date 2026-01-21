from django.shortcuts import render
from products.models import Category, Product
from pages.models import CustomerReview


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)[:8]
    reviews = CustomerReview.objects.filter(is_active=True)[:4]

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "reviews": reviews,   # ✅ now passed correctly
    })


def terms_of_service(request):
    return render(request, "pages/terms-of-service.html")


def shipping_policy(request):
    return render(request, "pages/shipping-policy.html")


def return_policy(request):
    return render(request, "pages/return-policy.html")


def privacy_policy(request):
    return render(request, "pages/privacy-policy.html")
