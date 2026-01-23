from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
import base64

from cart.cart import Cart
from .models import Order, OrderItem, BulkOrder


@login_required
def checkout_cod(request):
    cart = Cart(request)

    if cart.count() == 0:
        return redirect("/")

    if request.method == "POST":

        # 1️⃣ CREATE ORDER
        order = Order.objects.create(
            customer=request.user.customer,
            payment_type="COD",
            status="INITIATED",
            total_amount=cart.get_total_price(),
        )

        # 2️⃣ CREATE ORDER ITEMS
        for item in cart.get_items():

            order_item = OrderItem.objects.create(
                order=order,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"],
                custom_message=item.get("custom_message", ""),
            )

            # ✅ STEP 5 — DECODE BASE64 & SAVE IMAGE
            if item.get("custom_image"):
                image_data = base64.b64decode(item["custom_image"])
                image_name = item.get("custom_image_name", "custom.png")

                order_item.custom_image.save(
                    image_name,
                    ContentFile(image_data),
                    save=True
                )

        # 3️⃣ CLEAR CART (SESSION CLEAN)
        cart.clear()

        return render(
            request,
            "orders/thank_you.html",
            {"order": order}
        )

    return render(
        request,
        "orders/checkout_cod.html",
        {
            "cart_items": cart.get_items(),
            "total": cart.get_total_price(),
        }
    )


def bulk_order_view(request):
    context = {
        "active_nav": "bulk",  # 🔥 required for navbar underline
    }
    if request.method == "POST":
        BulkOrder.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("message"),
        )
        return render(request, "orders/bulk_order.html", {
            "success": True,
        })

    return render(request, "orders/bulk_order.html")