from django.urls import path
from .views import checkout_cod

urlpatterns = [
    path('cod/', checkout_cod, name='checkout_cod'),
]
