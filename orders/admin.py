from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, BulkOrder

# Branding
admin.site.site_header = "ART GIFT"
admin.site.site_title = "ArtGift Admin"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    fields = (
        "product",
        "quantity",
        "price",
        "custom_message_preview",
        "custom_message_view",
        "custom_image_preview",
        "custom_image_view",
        "custom_image_download",
    )

    readonly_fields = fields

    # ─────────────────────────────
    # 📝 MESSAGE (COMPACT + VIEW)
    # ─────────────────────────────
    def custom_message_preview(self, obj):
        if obj.custom_message:
            return format_html(
                '<div style="max-width:180px; white-space:nowrap; '
                'overflow:hidden; text-overflow:ellipsis;">{}</div>',
                obj.custom_message
            )
        return "—"

    custom_message_preview.short_description = "Message"

    def custom_message_view(self, obj):
        if not obj.custom_message:
            return "—"

        return format_html(
            '<button type="button" '
            'onclick="alert({})" '
            'style="padding:4px 10px; background:#444; color:#fff; '
            'border-radius:6px; border:none; cursor:pointer;">'
            'View</button>',
            repr(obj.custom_message)
        )

    custom_message_view.short_description = "Details"

    # ─────────────────────────────
    # 🖼️ IMAGE (PREVIEW + VIEW + DOWNLOAD)
    # ─────────────────────────────
    def custom_image_preview(self, obj):
        if obj.custom_image:
            return format_html(
                '<img src="{}" '
                'style="height:70px; width:auto; border-radius:6px; '
                'border:1px solid #ddd;" />',
                obj.custom_image.url
            )
        return "—"

    custom_image_preview.short_description = "Preview"

    def custom_image_view(self, obj):
        if not obj.custom_image:
            return "—"

        return format_html(
            '<button type="button" '
            'onclick="window.open(\'{}\', \'_blank\', '
            '\'width=800,height=800,noopener,noreferrer\')" '
            'style="padding:4px 10px; background:#222; color:#fff; '
            'border-radius:6px; border:none; cursor:pointer;">'
            'View</button>',
            obj.custom_image.url
        )

    custom_image_view.short_description = "View"

    def custom_image_download(self, obj):
        if obj.custom_image:
            return format_html(
                '<a href="{}" download '
                'style="display:inline-block; padding:6px 10px; '
                'background:#0d6efd; color:#fff; border-radius:6px; '
                'text-decoration:none;">Download</a>',
                obj.custom_image.url
            )
        return "—"

    custom_image_download.short_description = "Download"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_display",        # 👈 AG-2402-9502 · Raj Patil
        "phone",
        "payment_type",
        "status",
        "total_amount",
        "is_repeat_order",
        "created_at",
    )

    list_filter = (
        "payment_type",
        "status",
        "is_repeat_order",
        "created_at",
    )

    search_fields = (
        "public_order_id",
        "phone",
        "email",
        "first_name",
        "last_name",
        "pincode",
        "city",
    )

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Customer", {
            "fields": (
                "phone",
                "email",
                "first_name",
                "last_name",
                "age_group",
            )
        }),
        ("Address", {
            "fields": (
                "address_line_1",
                "address_line_2",
                "landmark",
                "city",
                "state",
                "pincode",
                "country",
            )
        }),
        ("Order Details", {
            "fields": (
                "public_order_id",
                "payment_type",
                "status",
                "total_amount",
                "is_repeat_order",
                "order_tags",
                "checkout_source",
                "created_at",
            )
        }),
    )

    inlines = [OrderItemInline]

    # ─────────────────────────────
    # 🔥 CUSTOM DISPLAY COLUMN
    # ─────────────────────────────
    def order_display(self, obj):
        order_id = obj.public_order_id or f"AG-{obj.id}"
        name = f"{obj.first_name or ''} {obj.last_name or ''}".strip() or "—"

        return format_html(
            "<strong>{}</strong><br><span style='color:#888'>{}</span>",
            order_id,
            name
        )

    order_display.short_description = "Order / Name"
    order_display.admin_order_field = "public_order_id"


@admin.register(BulkOrder)
class BulkOrderAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "created_at")
    search_fields = ("name", "email", "phone")
