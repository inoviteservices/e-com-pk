from django.http import JsonResponse
from django.shortcuts import render
from products.models import Category, Product, HotSingle
from pages.models import CustomerReview, NewsletterSubscriber
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count


def home(request):

    categories = Category.objects.all()

    products = Product.objects.filter(
        is_active=True
    )[:8]

    reviews = CustomerReview.objects.filter(
        is_active=True
    )[:4]


    hot_singles = HotSingle.objects.filter(
        is_active=True,
        product__is_active=True
    ).select_related("product").annotate(
        avg_rating=Avg("product__reviews__rating"),
        review_count=Count("product__reviews")
    )[:8]


    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "reviews": reviews,
        "hot_singles": hot_singles,
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
        return JsonResponse({"success": False, "message": "You’re already on our list!"})

    NewsletterSubscriber.objects.create(email=email)
    return JsonResponse({"success": True, "message": "You’re in! We’ll keep you posted."})