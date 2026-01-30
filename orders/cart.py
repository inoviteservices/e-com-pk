from decimal import Decimal
from products.models import Product
import uuid


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = request.session.get("cart", {})
        request.session["cart"] = self.cart

    # ➕ ADD TO CART
    def add(self, product_id, quantity=1, custom_image=None, custom_message=""):
        product = Product.objects.get(id=product_id)

        # 🔑 unique key per customized item
        cart_key = (
            f"{product_id}_{uuid.uuid4().hex}"
            if custom_image
            else str(product_id)
        )

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                "cart_key": cart_key,
                "product_id": product.id,  # ALWAYS INT
                "title": product.title,
                "price": str(product.price),
                "quantity": quantity,
                "image": product.image.url if product.image else "",
                "custom_image": custom_image,
                "custom_message": custom_message,
            }
        else:
            self.cart[cart_key]["quantity"] += quantity

        self.save()

    # ➖ DECREASE QUANTITY
    def decrease(self, cart_key):
        if cart_key in self.cart:
            self.cart[cart_key]["quantity"] -= 1
            if self.cart[cart_key]["quantity"] <= 0:
                del self.cart[cart_key]
        self.save()

    # ❌ REMOVE ITEM COMPLETELY
    def remove(self, cart_key):
        if cart_key in self.cart:
            del self.cart[cart_key]
        self.save()

    # 🧹 CLEAR CART
    def clear(self):
        self.session["cart"] = {}
        self.save()

    def save(self):
        self.session.modified = True

    # 🔁 ITERABLE (FOR TEMPLATES)
    def __iter__(self):
        for item in self.cart.values():
            yield {
                **item,
                "price_decimal": Decimal(item["price"]),
                "total_price": Decimal(item["price"]) * item["quantity"],
            }

    # 🔢 TOTAL QUANTITY (NAVBAR BADGE)
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def count(self):
        return sum(item["quantity"] for item in self.cart.values())

    # 📦 ITEMS LIST (NO DB QUERIES)
    def get_items(self):
        return list(self.cart.values())

    # 💰 TOTAL CART PRICE
    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )
