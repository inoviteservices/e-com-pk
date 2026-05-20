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

    images = request.FILES.getlist("custom_images")

    message = request.POST.get("custom_message", "")

    if product.requires_custom_image and not images:
        return JsonResponse({
            "error": "Image is required"
        }, status=400)

    pdf_relative_path = None

    if images:

        MAX_IMAGES = 10
        MAX_TOTAL_MB = 30

        if len(images) > MAX_IMAGES:
            return JsonResponse({
                "error": f"Maximum {MAX_IMAGES} images allowed"
            }, status=400)

        total_size = sum(img.size for img in images)

        if total_size > MAX_TOTAL_MB * 1024 * 1024:
            return JsonResponse({
                "error": f"Total upload must be under {MAX_TOTAL_MB}MB"
            }, status=400)

        upload_dir = os.path.join(
            settings.MEDIA_ROOT,
            "temp_uploads"
        )

        os.makedirs(upload_dir, exist_ok=True)

        temp_paths = []

        # =====================================
        # SAVE ALL IMAGES
        # =====================================
        for image in images:

            try:

                image_bytes = image.read()

                buffer = BytesIO(image_bytes)

                img = Image.open(buffer)

                img.verify()

                buffer.seek(0)

                img = Image.open(buffer).convert("RGB")

            except Exception:

                return JsonResponse({
                    "error": "Invalid image file"
                }, status=400)

            filename = f"{uuid.uuid4()}.jpg"

            full_path = os.path.join(
                upload_dir,
                filename
            )

            img.save(
                full_path,
                "JPEG",
                quality=90,
                optimize=True
            )

            temp_paths.append(full_path)

        # =====================================
        # GENERATE PDF
        # =====================================
        pdf_filename = f"{uuid.uuid4()}.pdf"

        pdf_relative_path = f"temp_uploads/{pdf_filename}"

        pdf_full_path = os.path.join(
            settings.MEDIA_ROOT,
            pdf_relative_path
        )

        pdf_images = []

        for path in temp_paths:

            with Image.open(path) as img:

                pdf_images.append(
                    img.convert("RGB").copy()
                )

        if pdf_images:

            first_image = pdf_images[0]

            remaining_images = pdf_images[1:]

            first_image.save(
                pdf_full_path,
                "PDF",
                resolution=100.0,
                save_all=True,
                append_images=remaining_images
            )

        # =====================================
        # CLEANUP TEMP JPGS
        # =====================================
        for path in temp_paths:

            if os.path.exists(path):
                os.remove(path)

    # =====================================
    # VARIANT LOGIC
    # =====================================
    variant_id = request.POST.get("variant_id")

    if variant_id:

        variant = ProductVariant.objects.get(
            id=variant_id
        )

        cart.add(
            product_id=product_id,
            variant_id=variant_id,
            price=variant.price,
            size=variant.size,
            custom_image=pdf_relative_path,
            custom_message=message
        )

    else:

        cart.add(
            product_id=product_id,
            custom_image=pdf_relative_path,
            custom_message=message
        )

    return JsonResponse({
        "cart_count": cart.count(),
        "cart_items": cart.get_items(),
        "cart_total": cart.get_total_price(),
    })

