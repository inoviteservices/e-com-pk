from django.http import JsonResponse
from django.shortcuts import render
from products.models import Category, Product
from pages.models import CustomerReview, NewsletterSubscriber
from django.views.decorators.http import require_POST

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)[:8]
    reviews = CustomerReview.objects.filter(is_active=True)[:4]

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "reviews": reviews,
        "active_nav": "home",
    })


def terms_of_service(request):
    return render(request, "pages/terms-of-service.html")


def shipping_policy(request):
    return render(request, "pages/shipping-policy.html")


def return_policy(request):
    return render(request, "pages/return-policy.html")


def privacy_policy(request):
    return render(request, "pages/privacy-policy.html")

@require_POST
def subscribe_newsletter(request):
    email = request.POST.get("email")

    if not email:
        return JsonResponse({"success": False, "message": "Email required"})

    if NewsletterSubscriber.objects.filter(email=email).exists():
        return JsonResponse({"success": False, "message": "Already subscribed"})

    NewsletterSubscriber.objects.create(email=email)
    return JsonResponse({"success": True, "message": "Subscribed successfully!"})