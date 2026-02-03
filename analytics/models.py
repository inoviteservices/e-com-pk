from django.db import models


class CheckoutEvent(models.Model):
    STAGES = (
        ("CART", "Cart Viewed"),
        ("CHECKOUT", "Checkout Opened"),
        ("ADDRESS", "Address Filled"),
        ("PAYMENT", "Payment Selected"),
        ("SUCCESS", "Order Placed"),
        ("FAILED", "Payment Failed"),
    )

    session_id = models.CharField(max_length=100)
    stage = models.CharField(max_length=20, choices=STAGES)

    device = models.CharField(max_length=50, blank=True)
    source = models.CharField(max_length=50, blank=True)  # instagram/google/direct

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_id} - {self.stage}"


class PaymentAttempt(models.Model):
    payment_type = models.CharField(max_length=10)  # COD / PREPAID
    status = models.CharField(max_length=20)        # SUCCESS / FAILED
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    failure_reason = models.CharField(max_length=255, blank=True)
    device = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class RTOEvent(models.Model):
    order_id = models.IntegerField()
    payment_type = models.CharField(max_length=10)
    courier = models.CharField(max_length=50, blank=True)
    reason = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
