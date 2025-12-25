from django.urls import path
from .views import privacy_policy, return_policy, shipping_policy, terms_of_service

urlpatterns = [
    path("terms-of-service/", terms_of_service, name="terms"),
    path("shipping-policy/", shipping_policy, name="shipping-policy"),
    path("return-policy/", return_policy, name="return_policy"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
]
