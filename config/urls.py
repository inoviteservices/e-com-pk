from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🏠 CMS & HOME
    path('', include('pages.urls')),

    # 🛍 PRODUCTS
    path('products/', include('products.urls')),

    # 🛒 CART (AJAX)
    path('cart/', include('cart.urls')),

    path('', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
