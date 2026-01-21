from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("add-custom/<int:product_id>/", views.cart_add_custom, name="cart_add_custom"),
    path("remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("decrease/<int:product_id>/", views.cart_decrease, name="cart_decrease"),
]
