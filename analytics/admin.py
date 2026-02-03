from django.contrib import admin
from .models import CheckoutEvent, PaymentAttempt, RTOEvent


@admin.register(CheckoutEvent)
class CheckoutEventAdmin(admin.ModelAdmin):
    list_display = ("session_id", "stage", "device", "source", "created_at")
    list_filter = ("stage", "device", "source")
    search_fields = ("session_id",)


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ("payment_type", "status", "amount", "created_at")
    list_filter = ("payment_type", "status")


@admin.register(RTOEvent)
class RTOEventAdmin(admin.ModelAdmin):
    list_display = ("order_id", "payment_type", "courier", "created_at")
    list_filter = ("payment_type", "courier")
