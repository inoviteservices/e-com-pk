from django.db import models
from users.models import Customer
from products.models import Product

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('PREPAID', 'Prepaid'),
        ('COD', 'Cash on Delivery'),
    )

    STATUS_CHOICES = (
        ('INITIATED', 'Initiated'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INITIATED')
    is_repeat_order = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
