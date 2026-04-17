import os
import uuid
from PIL import Image

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from products.models import ProductVariant
from products.models import Product
from .cart import Cart

MAX_FILE_SIZE_MB = 5
import json



def cart_add(request, product_id):

    cart = Cart(request)

    # 🔥 SAFE JSON HANDLING
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, TypeError):
            data = {}
    else:
        data = {}

    variant_id = data.get("variant_id")

    # 🔥 VARIANT LOGIC
    if variant_id:
        try:
            variant = ProductVariant.objects.get(id=variant_id)

            cart.add(
                product_id=product_id,
                variant_id=variant_id,
                price=variant.price,
                size=variant.size
            )
        except ProductVariant.DoesNotExist:
            return JsonResponse({"error": "Invalid variant"}, status=400)

    else:
        cart.add(product_id=product_id)

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



from io import BytesIO


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

        # ✅ Size check
        if image.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            return JsonResponse({"error": "Image must be under 5MB"}, status=400)

        try:
            # ✅ Read once into memory
            image_bytes = image.read()
            buffer = BytesIO(image_bytes)

            img = Image.open(buffer)
            img.verify()

            # Reset buffer
            buffer.seek(0)
            img = Image.open(buffer)

        except Exception:
            return JsonResponse({"error": "Invalid image file"}, status=400)

        ext = image.name.split('.')[-1].lower()

        upload_dir = os.path.join(settings.MEDIA_ROOT, "temp_uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # 📌 Convert HEIC → JPG
        if ext in ["heic", "heif"]:

            try:
                img = img.convert("RGB")

                filename = f"{uuid.uuid4()}.jpg"
                full_path = os.path.join(upload_dir, filename)

                img.save(
                    full_path,
                    "JPEG",
                    quality=90,
                    optimize=True
                )

            except Exception:
                return JsonResponse({"error": "Failed to process image"}, status=400)

        else:
            # Save other formats

            filename = f"{uuid.uuid4()}.{ext}"
            full_path = os.path.join(upload_dir, filename)

            with open(full_path, "wb") as f:
                f.write(image_bytes)

        temp_path = f"temp_uploads/{filename}"
    variant_id = request.POST.get("variant_id")
    if variant_id:
        variant = ProductVariant.objects.get(id=variant_id)

        cart.add(
            product_id=product_id,
            variant_id=variant_id,
            price=variant.price,
            size=variant.size,
            custom_image=temp_path,
            custom_message=message
        )
    else:
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
