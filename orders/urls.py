from django.urls import path
from .views import checkout, bulk_order_view

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path("bulk-orders/", bulk_order_view, name="bulk_orders"),
]
