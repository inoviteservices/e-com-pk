# cart/context_processors.py

from .cart import Cart

def cart_context(request):
    cart = Cart(request)
    return {
        "cart": cart,
        "cart_items": cart,
        "cart_count": cart.__len__(),
        "cart_total": cart.get_total_price(),
    }
