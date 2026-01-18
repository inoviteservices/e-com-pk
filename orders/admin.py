from django.contrib import admin

# Register your models here.

admin.site.site_header = "ART GIFT"
admin.site.site_title = "artgift"
# admin.site.index_title = "artgift dashboard"
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'payment_type', 'status', 'total_amount', 'created_at')
    list_filter = ('payment_type', 'status')
    inlines = [OrderItemInline]
