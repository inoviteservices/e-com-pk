from django.urls import path
from .views import (
    about_us,
    home,
    privacy_policy,
    return_policy,
    shipping_policy,
    terms_of_service,
    subscribe_newsletter,
)

urlpatterns = [
    path("", home, name="home"),

    path("terms-of-service/", terms_of_service, name="terms"),
    path("shipping-policy/", shipping_policy, name="shipping_policy"),
    path("refund-and-replacement/", return_policy, name="return_policy"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("about-us/", about_us, name="about_us"),
    path("subscribe/", subscribe_newsletter, name="subscribe_newsletter"),
]
