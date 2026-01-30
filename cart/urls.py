from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:product_id>/", views.cart_add),
    path("add-custom/<int:product_id>/", views.cart_add_custom),

    # 🔥 THESE MUST USE cart_key (string)
    path("decrease/<str:cart_key>/", views.cart_decrease),
    path("remove/<str:cart_key>/", views.cart_remove),
]
