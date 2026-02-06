import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files import File

from cart.cart import Cart
from .models import Order, OrderItem, BulkOrder


# ============================
# CHECKOUT
# ============================

def checkout(request):

    cart = Cart(request)

    # ❌ Block empty cart
    if cart.count() == 0:
        return redirect("/")

    if request.method == "POST":

        # --------------------
        # CONTACT
        # --------------------
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        # Repeat buyer check
        is_repeat = Order.objects.filter(phone=phone).exists()

        # --------------------
        # PAYMENT LOGIC
        # --------------------
        cart_total = cart.get_total_price()

        # Get payment type
        payment_type = request.POST.get("payment_type", "COD")

        final_amount = cart_total

        # Apply charges / discounts
        if payment_type == "COD":
            final_amount += 49

        elif payment_type == "PREPAID":
            final_amount -= 50

        # Safety (no negative)
        if final_amount < 0:
            final_amount = 0


        # --------------------
        # CREATE ORDER
        # --------------------
        order = Order.objects.create(

            phone=phone,
            email=email,

            first_name=request.POST.get("first_name", "N/A"),
            last_name=request.POST.get("last_name", "N/A"),

            address_line_1=request.POST.get("address1", "N/A"),
            address_line_2=request.POST.get("address2", "N/A"),
            landmark=request.POST.get("landmark", ""),

            city=request.POST.get("city", "N/A"),
            state=request.POST.get("state", "N/A"),
            pincode=request.POST.get("pincode", "000000"),
            country="India",


            payment_type=payment_type,      # ✅ dynamic
            status="INITIATED",
            total_amount=final_amount,      # ✅ correct total

            is_repeat_order=is_repeat,
            order_tags=["Repeat Buyer"] if is_repeat else [],
            checkout_source="website",
        )


        # --------------------
        # CREATE ORDER ITEMS
        # --------------------
        for item in cart.get_items():

            order_item = OrderItem.objects.create(

                order=order,

                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"],

                custom_message=item.get("custom_message", ""),
            )


            # --------------------
            # SAVE CUSTOM IMAGE
            # --------------------
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

                    # Delete temp file
                    os.remove(full_path)


        # --------------------
        # CLEAR CART
        # --------------------
        cart.clear()


        # --------------------
        # THANK YOU
        # --------------------
        return render(
            request,
            "orders/thank_you.html",
            {"order": order}
        )


    # ============================
    # GET REQUEST
    # ============================
    return render(
        request,
        "orders/checkout.html",
        {
            "cart_items": cart.get_items(),
            "total": cart.get_total_price(),
        }
    )



# ============================
# BULK ORDER
# ============================

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



# ============================
# TRACK ORDER
# ============================

ORDER_STEPS = ["INITIATED", "PAID", "SHIPPED", "DELIVERED"]


def track_order(request):

    order = None
    error = None

    if request.method == "POST":

        order_id = request.POST.get("order_id", "").strip().upper()

        try:
            order = Order.objects.get(public_order_id=order_id)

        except Order.DoesNotExist:

            error = "Order not found. Please check your Order ID."


    return render(
        request,
        "orders/track_order.html",
        {
            "order": order,
            "error": error,
            "steps": ORDER_STEPS,
        }
    )
