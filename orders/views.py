from django.http import JsonResponse
from .cart import Cart

def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return JsonResponse({
        "cart_count": cart.count(),
        "cart_items": cart.get_items(),
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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

@login_required
def checkout_cod(request):
    cart = Cart(request)

    if cart.count() == 0:
        return redirect('/')

    if request.method == "POST":
        order = Order.objects.create(
            customer=request.user.customer,
            payment_type='COD',
            status='INITIATED',
            total_amount=cart.get_total_price()
        )

        for item in cart.get_items():
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        cart.clear()
        return render(request, "orders/thank_you.html", {"order": order})

    return render(request, "orders/checkout_cod.html", {
        "cart_items": cart.get_items(),
        "total": cart.get_total_price()
    })
