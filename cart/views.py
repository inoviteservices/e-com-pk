import os
import uuid
from PIL import Image

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from products.models import Product
from .cart import Cart

MAX_FILE_SIZE_MB = 5


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

    # Check if image is required
    if product.requires_custom_image and not image:
        return JsonResponse({"error": "Image is required"}, status=400)

    temp_path = None

    if image:

        # ✅ Max size: 5MB
        if image.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            return JsonResponse({"error": "Image must be under 5MB"}, status=400)

        # ✅ Validate image
        try:
            img = Image.open(image)
            image.seek(0)
        except Exception:
            return JsonResponse({"error": "Invalid image file"}, status=400)

        # Get extension
        ext = image.name.split('.')[-1].lower()

        # Upload folder
        upload_dir = os.path.join(settings.MEDIA_ROOT, "temp_uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # 📌 Convert HEIC/HEIF → JPG
        if ext in ["heic", "heif"]:

            try:
                img = Image.open(image)
                img = img.convert("RGB")

                filename = f"{uuid.uuid4()}.jpg"
                full_path = os.path.join(upload_dir, filename)

                img.save(
                    full_path,
                    format="JPEG",
                    quality=90,
                    optimize=True
                )

            except Exception:
                return JsonResponse({"error": "Failed to process image"}, status=400)

        else:
            # Save normally (jpg/png/etc)

            filename = f"{uuid.uuid4()}.{ext}"
            full_path = os.path.join(upload_dir, filename)

            with open(full_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)

        # Relative path for media
        temp_path = f"temp_uploads/{filename}"

    # Add to cart
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
