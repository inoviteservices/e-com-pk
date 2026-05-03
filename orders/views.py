import os
from urllib import request
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files import File
from .services_sms import send_order_confirmation_sms
from .services_sms import send_cod_otp_sms
from cart.cart import Cart
from .models import Order, OrderItem, BulkOrder
from .services import create_cashfree_order, verify_cashfree_payment
import random
import time
from products.models import Product  # add at top if not already
from .services_delhivery import create_delhivery_shipment
from orders.meta import send_meta_event
import uuid
# ============================
# CHECKOUT
# ============================


def verify_cod_otp(request):

    if request.method == "POST":
        user_otp = request.POST.get("otp")

        if time.time() - request.session.get("otp_time", 0) > 300:
            return render(request, "orders/verify_otp.html", {"error": "OTP expired"})

        if user_otp == request.session.get("cod_otp"):

            data = request.session.get("cod_order_data")
            cart_items = request.session.get("cart_data")

            # 🔥 FIX START
            phone = str(data.get("phone"))[-10:]
            existing_orders = Order.objects.filter(phone=phone).count()
            is_repeat = existing_orders > 0
            # 🔥 FIX END

            order = Order.objects.create(
                phone=phone,
                email=data.get("email"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                address_line_1=data.get("address1"),
                address_line_2=data.get("address2"),
                landmark=data.get("landmark"),
                city=data.get("city"),
                state=data.get("state"),
                pincode=data.get("pincode"),
                country="India",
                payment_type="COD",
                status="PAID",
                payment_status="SUCCESS",
                total_amount=request.session.get("final_amount", 0),
                is_repeat_order=is_repeat   # 🔥 THIS FIXES YOUR ISSUE
            )

            for item in cart_items:

                order_item = OrderItem.objects.create(   # 🔥 STORE OBJECT
                    order=order,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"],
                    custom_message=item.get("custom_message", "")
                )

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

                        os.remove(full_path)  # optional cleanup

            send_order_confirmation_sms(order)
            create_delhivery_shipment(order)


           

            # event_id = str(uuid.uuid4())
            event_id = f"order_{order.public_order_id}"

            response = send_meta_event(
                email=order.email,
                value=order.total_amount,
                event_name="Purchase",
                event_id=event_id
            )

            print("META STATUS:", response)

            request.session.flush()

            cart = Cart(request)
            cart.clear()

            return render(request, "orders/thank_you.html", {"order": order})

        else:
            return render(request, "orders/verify_otp.html", {"error": "Invalid OTP"})
        
        
        
def checkout(request):

    cart = Cart(request)

    if cart.count() == 0:
        return redirect("/")

    if request.method == "POST":

        # --------------------
        # CONTACT
        # --------------------
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        is_repeat = Order.objects.filter(phone=phone).exists()

        # --------------------
        # PAYMENT LOGIC
        # --------------------
        cart_total = cart.get_total_price()
        payment_type = request.POST.get("payment_type", "COD")

        final_amount = cart_total

        if payment_type == "COD":
            final_amount += 49
        elif payment_type == "PREPAID":
            final_amount -= 50

        if final_amount < 0:
            final_amount = 0

        # ============================
        # COD FLOW (OTP FIRST)
        # ============================
        if payment_type == "COD":

            otp = random.randint(100000, 999999)

            request.session["cod_otp"] = str(otp)
            request.session["otp_time"] = time.time()
            request.session["cod_order_data"] = request.POST.dict()

            clean_cart = []

            for item in cart.get_items():
                clean_cart.append({
                    "product_id": item.get("product_id"),
                    "quantity": item.get("quantity", 0),
                    "price": float(item.get("price", 0)),
                    "custom_message": item.get("custom_message", ""),
                    "custom_image": item.get("custom_image")   # 🔥 ADD THIS

                })

            request.session["cart_data"] = clean_cart
            request.session["final_amount"] = float(final_amount)

            send_cod_otp_sms(phone, otp)

            # return render(request, "orders/verify_otp.html")
            return render(request, "orders/verify_otp.html", {
                "phone": phone
            })

        # ============================
        # PREPAID FLOW (CREATE ORDER)
        # ============================

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
            payment_type="PREPAID",
            status="INITIATED",
            payment_status="PENDING",
            total_amount=float(final_amount),
            is_repeat_order=is_repeat,
            order_tags=["Repeat Buyer"] if is_repeat else [],
            checkout_source="website",
        )

        # --------------------
        # CREATE ITEMS
        # --------------------
        for item in cart.get_items():

            order_item = OrderItem.objects.create(
                order=order,
                product_id=item.get("product_id"),
                quantity=item.get("quantity", 0),
                price=float(item.get("price", 0)),
                custom_message=item.get("custom_message", "")
            )

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
                    os.remove(full_path)

        # --------------------
        # CASHFREE
        # --------------------
        response = create_cashfree_order(order)
        print("🔥 SESSION:", response.get("payment_session_id") if response else "NO RESPONSE")
        

        if not response or not isinstance(response, dict) or "payment_session_id" not in response:
            order.payment_status = "FAILED"
            order.save()

            return render(request, "orders/payment_failed.html", {
                "order": order,
                "error": "Payment initialization failed"
            })

        order.gateway_order_id = response.get("order_id")
        order.payment_gateway = "cashfree"
        order.status = "PENDING_PAYMENT"
        order.save()

        return render(request, "orders/cashfree_payment.html", {
            "payment_session_id": response.get("payment_session_id"),
            "order_id": order.public_order_id,
            "cashfree_mode": settings.CASHFREE_MODE   
        })

    # ============================
    # FIXED GET RESPONSE (IMPORTANT)
    # ============================

    cart_items = []

    for item in cart.get_items():
        try:
            product = Product.objects.get(id=item.get("product_id"))
        except Product.DoesNotExist:
            continue

        cart_items.append({
            "product": product,
            "quantity": item.get("quantity", 0),
            "price": float(item.get("price", 0)),
            "custom_message": item.get("custom_message", ""),
        })

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total": float(cart.get_total_price()),
    })



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

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


@csrf_exempt
def cashfree_webhook(request):

    try:
        data = json.loads(request.body)

        order_id = data["data"]["order"]["order_id"]
        payment_status = data["data"]["payment"]["payment_status"]
        payment_id = data["data"]["payment"]["cf_payment_id"]

        try:
            order = Order.objects.get(public_order_id=order_id)
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)

        # 🔁 Prevent duplicate processing
        if order.payment_status == "SUCCESS" and order.status == "PAID":

            return HttpResponse("Already processed")

        # ✅ SUCCESS
        if payment_status == "SUCCESS":
            order.payment_status = "SUCCESS"
            order.status = "PAID"

            # 🚀 NEXT STEP (VERY IMPORTANT)
            # send_sms(order)
            send_order_confirmation_sms(order)
            create_delhivery_shipment(order)


            # event_id = str(uuid.uuid4())
            event_id = f"order_{order.public_order_id}"

            response = send_meta_event(
                email=order.email,
                value=order.total_amount,
                event_name="Purchase",
                event_id=event_id
            )

            print("META STATUS:", response)

        # ❌ USER DROPPED / NOT ATTEMPTED
        elif payment_status in ["USER_DROPPED", "NOT_ATTEMPTED"]:
            order.payment_status = "CANCELLED"

        # ❌ FAILED / CANCELLED / VOID
        elif payment_status in ["FAILED", "CANCELLED", "VOID"]:
            order.payment_status = "FAILED"

        # ⏳ PENDING
        else:
            order.payment_status = "PENDING"

        order.gateway_payment_id = payment_id
        order.save()

        print(f"🔥 WEBHOOK: {order_id} → {payment_status}")

    except Exception as e:
        print("❌ WEBHOOK ERROR:", str(e))

    return HttpResponse("OK")

def payment_result(request):

    order_id = request.GET.get("order_id")

    if not order_id:
        return render(request, "orders/payment_failed.html")

    try:
        order = Order.objects.get(public_order_id=order_id)
    except Order.DoesNotExist:
        return render(request, "orders/payment_failed.html")

    # 🔥 ALWAYS VERIFY IF NOT SUCCESS (not just PENDING)
    if order.payment_status == "PENDING" and not order.gateway_payment_id:

        verify_data = verify_cashfree_payment(order.public_order_id)

        if verify_data and verify_data.get("data"):
            for p in verify_data.get("data", []):

                status = p.get("payment_status")

                if status == "SUCCESS":
                    order.payment_status = "SUCCESS"
                    order.status = "PAID"

                elif status in ["FAILED", "CANCELLED", "VOID"]:
                    order.payment_status = "FAILED"

                elif status in ["USER_DROPPED", "NOT_ATTEMPTED"]:
                    order.payment_status = "CANCELLED"

                order.gateway_payment_id = p.get("cf_payment_id")
                order.save()
                break

    # ✅ SUCCESS
    if order.payment_status == "SUCCESS":
        cart = Cart(request)
        cart.clear()
        return render(request, "orders/thank_you.html", {"order": order})

    # ❌ FAILED
    elif order.payment_status == "FAILED":
        return render(request, "orders/payment_failed.html", {"order": order})

    # ❌ CANCELLED
    elif order.payment_status == "CANCELLED":
        return render(request, "orders/payment_cancelled.html", {"order": order})

    # ⏳ STILL PENDING
    else:
        return render(request, "orders/payment_pending.html", {"order": order})