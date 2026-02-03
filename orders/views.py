import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files import File

from cart.cart import Cart
from .models import Order, OrderItem, BulkOrder


def checkout(request):
    cart = Cart(request)

    # ❌ Block empty cart checkout
    if cart.count() == 0:
        return redirect("/")

    if request.method == "POST":

        # 🔹 CONTACT
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        # 🔁 Repeat buyer detection (analytics core)
        is_repeat = Order.objects.filter(phone=phone).exists()

        # 🔹 CREATE ORDER
        order = Order.objects.create(
            phone=phone,
            email=email,

            first_name=request.POST.get("first_name", "N/A"),
            last_name=request.POST.get("last_name", "N/A"),

            address_line_1=request.POST.get("address_line_1", "N/A"),
            address_line_2=request.POST.get("address_line_2", "N/A"),
            landmark=request.POST.get("landmark", ""),

            city=request.POST.get("city", "N/A"),
            state=request.POST.get("state", "N/A"),
            pincode=request.POST.get("pincode", "000000"),
            country="India",

            age_group=request.POST.get("age_group", "N/A"),

            payment_type="COD",
            status="INITIATED",
            total_amount=cart.get_total_price(),

            is_repeat_order=is_repeat,
            order_tags=["Repeat Buyer"] if is_repeat else [],
            checkout_source="website",
        )

        # 🔹 CREATE ORDER ITEMS
        for item in cart.get_items():

            order_item = OrderItem.objects.create(
                order=order,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"],
                custom_message=item.get("custom_message", ""),
            )

            # ✅ SAVE CUSTOM IMAGE (CORRECT WAY)
            temp_path = item.get("custom_image")

            if temp_path:
                full_path = os.path.join(settings.MEDIA_ROOT, temp_path)

                if os.path.exists(full_path):
                    with open(full_path, "rb") as f:
                        order_item.custom_image.save(
                            os.path.basename(full_path),
                            File(f),
                            save=True
                        )

                    # 🧹 Remove temp file after saving
                    os.remove(full_path)

        # 🔹 CLEAR CART
        cart.clear()

        return render(
            request,
            "orders/thank_you.html",
            {"order": order}
        )

    # 🔹 GET REQUEST
    return render(
        request,
        "orders/checkout.html",
        {
            "cart_items": cart.get_items(),
            "total": cart.get_total_price(),
        }
    )


def bulk_order_view(request):
    if request.method == "POST":
        BulkOrder.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("message"),
        )
        return render(
            request,
            "orders/bulk_order.html",
            {"success": True}
        )

    return render(request, "orders/bulk_order.html")
