from decimal import Decimal
from products.models import Product
import base64

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get("cart")

        if not self.cart:
            self.cart = self.session["cart"] = {}

    def add(self, product_id, custom_image=None, custom_message=""):
        product = Product.objects.get(id=product_id)
        pid = str(product_id)

        if pid not in self.cart:
            self.cart[pid] = {
                "product_id": product.id,
                "title": product.title,
                "price": str(product.price),
                "quantity": 1,
                "custom_message": custom_message,
                "custom_image": None,
                "custom_image_name": None,
            }

            # ✅ STEP 4: SESSION-SAFE IMAGE STORAGE
            if custom_image:
                encoded = base64.b64encode(custom_image.read()).decode("utf-8")
                self.cart[pid]["custom_image"] = encoded
                self.cart[pid]["custom_image_name"] = custom_image.name

        self.session.modified = True

    def get_items(self):
        items = []

        for item in self.cart.values():
            product = Product.objects.get(id=item["product_id"])

            items.append({
                "product_id": product.id,
                "title": product.title,
                "price": Decimal(item["price"]),
                "quantity": item["quantity"],
                "category": product.category.name if product.category else "",
                "image": product.image.url if product.image else "",
                "custom_message": item.get("custom_message", ""),
                "custom_image": item.get("custom_image"),
                "custom_image_name": item.get("custom_image_name"),
            })

        return items

    def count(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True
