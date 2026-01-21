from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from products.models import Product
from .cart import Cart
from PIL import Image

MAX_FILE_SIZE_MB = 5
ALLOWED_FORMATS = ["JPEG", "PNG"]


def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return JsonResponse({
    "cart_count": cart.count(),
    "cart_total": cart.get_total_price(),
})


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return JsonResponse({
        "cart_count": cart.count(),
        "cart_items": cart.get_items(),
        "cart_total": cart.get_total_price(),
    })


def cart_decrease(request, product_id):
    cart = Cart(request)
    cart.decrease(product_id)

    return JsonResponse({
        "cart_count": cart.count(),
        "cart_items": cart.get_items(),
        "cart_total": cart.get_total_price(),
    })


def cart_add_custom(request, product_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    image = request.FILES.get("custom_image")
    message = request.POST.get("custom_message", "")

    # OPTIONAL: only if field exists
    if hasattr(product, "requires_custom_image") and product.requires_custom_image and not image:
        return JsonResponse(
            {"error": "This product requires an image upload."},
            status=400
        )

    if image:
        if image.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            return JsonResponse({"error": "Image must be under 5MB."}, status=400)

        try:
            img = Image.open(image)
            img.verify()
            image.seek(0)
            img = Image.open(image)
        except Exception:
            return JsonResponse({"error": "Invalid image file."}, status=400)

        if img.format not in ALLOWED_FORMATS:
            return JsonResponse({"error": "Only JPG and PNG images allowed."}, status=400)

        width, height = img.size
        if width < 300 or height < 300:
            return JsonResponse({"error": "Minimum image size is 300×300 px."}, status=400)

        if width > 5000 or height > 5000:
            return JsonResponse({"error": "Maximum image size is 5000×5000 px."}, status=400)

    cart.add(
        product_id=product_id,
        custom_image=image,
        custom_message=message
    )

    return JsonResponse({
        "cart_count": cart.count(),
        "cart_total": cart.get_total_price(),
    })
