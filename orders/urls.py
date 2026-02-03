from django.urls import path
from .views import checkout, bulk_order_view, track_order

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path("bulk-orders/", bulk_order_view, name="bulk_orders"),
    path("track-order/", track_order, name="track_order"),
]
