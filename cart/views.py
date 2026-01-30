import os
import uuid
from PIL import Image

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from products.models import Product
from .cart import Cart

MAX_FILE_SIZE_MB = 5
ALLOWED_FORMATS = ["JPEG", "PNG"]


def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return JsonResponse({
        "cart_count": cart.count(),
        "cart_items": cart.get_items(),
        "cart_total": cart.get_total_price(),
    })



def cart_decrease(request, cart_key):
    cart = Cart(request)
    cart.decrease(cart_key)

    return JsonResponse({
        "cart_count": cart.count(),
        "cart_items": cart.get_items(),
        "cart_total": cart.get_total_price(),
    })


def cart_remove(request, cart_key):
    cart = Cart(request)
    cart.remove(cart_key)

    return JsonResponse({
        "cart_count": cart.count(),
        "cart_items": cart.get_items(),   # prices are strings → OK
        "cart_total": str(cart.get_total_price()),  # ✅ FIX
    })



def cart_add_custom(request, product_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=405)

    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    image = request.FILES.get("custom_image")
    message = request.POST.get("custom_message", "")

    if product.requires_custom_image and not image:
        return JsonResponse({"error": "Image is required"}, status=400)

    temp_path = None

    if image:
        if image.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            return JsonResponse({"error": "Max file size is 5MB"}, status=400)

        try:
            img = Image.open(image)
            img.verify()
            image.seek(0)
            img = Image.open(image)
        except Exception:
            return JsonResponse({"error": "Invalid image file"}, status=400)

        if img.format not in ALLOWED_FORMATS:
            return JsonResponse({"error": "Only JPG and PNG allowed"}, status=400)

        if img.width < 300 or img.height < 300:
            return JsonResponse({"error": "Minimum size 300×300"}, status=400)

        filename = f"{uuid.uuid4()}.{image.name.split('.')[-1]}"
        temp_path = f"temp_uploads/{filename}"
        full_path = os.path.join(settings.MEDIA_ROOT, temp_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "wb+") as f:
            for chunk in image.chunks():
                f.write(chunk)

    cart.add(
        product_id=product_id,
        custom_image=temp_path,
        custom_message=message
    )

    return JsonResponse({
        "cart_count": cart.count(),
        "cart_items": cart.get_items(),
        "cart_total": cart.get_total_price(),
    })
