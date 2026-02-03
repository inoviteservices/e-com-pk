import random
from django.db import models
from products.models import Product
from datetime import datetime


class Order(models.Model):

    PAYMENT_CHOICES = (
        ("PREPAID", "Prepaid"),
        ("COD", "Cash on Delivery"),
    )

    STATUS_CHOICES = (
        ("INITIATED", "Initiated"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )

    # 🔹 PUBLIC ORDER ID (NEW)
    public_order_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    # 🔹 CONTACT
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # 🔹 NAME
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    # 🔹 ADDRESS
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)

    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    # 🔹 EXTRA
    age_group = models.CharField(max_length=20, null=True, blank=True)
    is_repeat_order = models.BooleanField(default=False)

    order_tags = models.JSONField(default=list, blank=True)
    checkout_source = models.CharField(max_length=50, null=True, blank=True)

    # 🔹 PAYMENT
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="COD"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="INITIATED"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 AUTO GENERATE ORDER ID
    def save(self, *args, **kwargs):
        if not self.public_order_id:
            month_year = datetime.now().strftime("%m%y")  # 0226
            while True:
                candidate = f"AG-{month_year}-{random.randint(1000, 9999)}"
                if not Order.objects.filter(public_order_id=candidate).exists():
                    self.public_order_id = candidate
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.public_order_id or f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    custom_image = models.ImageField(
        upload_to="orders/custom/",
        null=True,
        blank=True
    )
    custom_message = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"

class BulkOrder(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bulk Order - {self.name}"
