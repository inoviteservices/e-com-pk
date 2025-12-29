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
