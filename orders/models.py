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
        ("PENDING_PAYMENT", "Pending Payment"),
        ("PAID", "Paid"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled"),
    )

    # 🔹 PUBLIC ORDER ID
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
    is_repeat_order = models.BooleanField(default=False)

    order_tags = models.JSONField(default=list, blank=True)
    checkout_source = models.CharField(max_length=50, null=True, blank=True)

    # 🔹 PAYMENT TYPE
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="COD"
    )

    # 🔹 ORDER STATUS
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

    # 🔹 PAYMENT GATEWAY DATA
    payment_gateway = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    gateway_order_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    gateway_payment_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    payment_status = models.CharField(
        max_length=20,
        default="PENDING"
    )

    paid_at = models.DateTimeField(null=True, blank=True)

    # 🔹 SHIPPING
    tracking_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    courier_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    shipping_status = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    # 🔹 SMS TRACKING
    sms_sent = models.BooleanField(default=False)
    sms_sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 AUTO GENERATE ORDER ID
    def save(self, *args, **kwargs):
        if not self.public_order_id:
            month_year = datetime.now().strftime("%m%y")
            while True:
                candidate = f"AG{month_year}{random.randint(1000, 9999)}"
                if not Order.objects.filter(public_order_id=candidate).exists():
                    self.public_order_id = candidate
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.public_order_id or f"Order #{self.id}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["public_order_id"]),
            models.Index(fields=["phone"]),
        ]


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

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