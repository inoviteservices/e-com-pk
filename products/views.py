from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, CustomerReview
from django.db.models import Avg, Count, Value
from django.db.models.functions import Coalesce
import random
from django.http import JsonResponse


def search_suggestions(request):

    q = request.GET.get("q", "").strip()

    if not q:
        return JsonResponse([], safe=False)

    products = Product.objects.filter(
        is_active=True,
        title__icontains=q
    ).values("title", "slug")[:6]   # max 6 results

    return JsonResponse(list(products), safe=False)


# Optional: redirect old URLs safely
def category_redirect(request, slug):
    return redirect(f"/products/category/all/?category={slug}")




def shop_all(request):
    categories = Category.objects.all()

    products = Product.objects.filter(
        is_active=True
    ).annotate(
        avg_rating=Coalesce(Avg("reviews__rating"), Value(0.0)),
        total_reviews=Count("reviews", distinct=True)
    )

    active_category = request.GET.get("category")

    if active_category:
        products = products.filter(category__slug=active_category)

    # optional but recommended
    products = products.order_by("-total_reviews")

    return render(request, "products/shop_all.html", {
        "categories": categories,
        "products": products,
        "active_category": active_category,
        "active_nav": "shop",
    })
def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug, is_active=True)

    variants = product.variants.filter(is_active=True)

    # Fake interest count
    interest_count = (product.id % 5) + random.randint(6, 18)

    # ✅ SAVE REVIEW (NEW PART)
    if request.method == "POST":

        name = request.POST.get("name")
        rating = request.POST.get("rating")
        review_text = request.POST.get("review")
        media = request.FILES.get("media")


        if name and rating and review_text:

            CustomerReview.objects.create(
                product=product,
                name=name.strip(),
                rating=int(rating),
                review=review_text.strip(),
                media=media,
                is_active=True,
            )

        return redirect(request.path)  # avoid resubmission


    # Reviews
    reviews = product.reviews.filter(is_active=True)

    total_reviews = reviews.count()

    avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    avg_rating = round(avg_rating, 2)

    # Star counts
    star_counts = {
        5: reviews.filter(rating=5).count(),
        4: reviews.filter(rating=4).count(),
        3: reviews.filter(rating=3).count(),
        2: reviews.filter(rating=2).count(),
        1: reviews.filter(rating=1).count(),
    }

    # Star percentages (for bars)
    star_percentages = {}

    for star, count in star_counts.items():
        if total_reviews > 0:
            star_percentages[star] = int((count / total_reviews) * 100)
        else:
            star_percentages[star] = 0

    return render(request, "product_detail.html", {
        "product": product,
        "interest_count": interest_count,
        "variants": variants,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "total_reviews": total_reviews,

        "star_counts": star_counts,
        "star_percentages": star_percentages,
    })
