from django.shortcuts import redirect, render
from .cart import Cart
from products.models import Product

def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart')


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {
        'cart_items': cart.get_items(),
        'total': cart.get_total_price()
    })

def cart_decrease(request, product_id):
    cart = Cart(request)
    product_id = str(product_id)

    if product_id in cart.cart:
        if cart.cart[product_id]['quantity'] > 1:
            cart.cart[product_id]['quantity'] -= 1
        else:
            del cart.cart[product_id]
        cart.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))
