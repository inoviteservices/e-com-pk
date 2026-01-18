from django.urls import path
from . import views
from .views import checkout_cod


urlpatterns = [
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/decrease/<int:product_id>/', views.cart_decrease, name='cart_decrease'),
    path("checkout/", checkout_cod, name="checkout"),



]
