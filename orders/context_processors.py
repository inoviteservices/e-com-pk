from .cart import Cart

def cart_context(request):
    cart = Cart(request)
    items = cart.get_items()

    return {
        'cart_items': items,
        'cart_total': cart.get_total_price(),
        'cart_count': sum(item['quantity'] for item in items)
    }
