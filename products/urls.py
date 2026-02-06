from django.urls import path
from . import views

urlpatterns = [
    path("category/all/", views.shop_all, name="shop_all"),

    # TEMPORARY safety redirect (optional but recommended)
    path("category/<slug:slug>/", views.category_redirect),
    path("search-suggestions/", views.search_suggestions, name="search_suggestions"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
]
