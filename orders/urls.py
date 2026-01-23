from django.urls import path
from .views import checkout_cod, bulk_order_view

urlpatterns = [
    path('cod/', checkout_cod, name='checkout_cod'),
    path("bulk-orders/", bulk_order_view, name="bulk_orders"),
]
