from .cart import Cart

def cart_context(request):
    cart = Cart(request)
    return {
        'cart_items': cart.get_items(),
        'cart_total': cart.get_total_price(),
        'cart_count': sum(item['quantity'] for item in cart.get_items())
    }
