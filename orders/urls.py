from django.urls import path
from .views import checkout, bulk_order_view, delhivery_webhook, track_order, cashfree_webhook, payment_result, verify_cod_otp

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path("bulk-orders/", bulk_order_view, name="bulk_orders"),
    path("track-order/", track_order, name="track_order"),
    path("cashfree/webhook/", cashfree_webhook, name="cashfree_webhook"),
    path("payment-result/", payment_result, name="payment_result"),
    path('verify-otp/', verify_cod_otp, name='verify_cod_otp'),
    path("webhook/delhivery/", delhivery_webhook),
]
