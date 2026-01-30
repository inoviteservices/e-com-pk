from .cart import Cart

def cart_context(request):
    cart = Cart(request)

    return {
        "cart": cart,                         # full cart object (for methods)
        "cart_items": list(cart),             # iterable items (SAFE)
        "cart_count": len(cart),              # pythonic
        "cart_total": cart.get_total_price(), # Decimal-safe
    }
