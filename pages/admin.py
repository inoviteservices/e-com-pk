from django.contrib import admin
from django.utils.html import format_html

from .models import (
    SiteLogo,
    SiteAnnouncement,
    HeroSlide,
    CustomerReview,
    NewsletterSubscriber,   # ✅ NEW
)

# ------------------------
# SITE LOGO
# ------------------------

@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only one logo allowed
        return not SiteLogo.objects.exists()


# ------------------------
# SITE ANNOUNCEMENT
# ------------------------

@admin.register(SiteAnnouncement)
class SiteAnnouncementAdmin(admin.ModelAdmin):

    list_display = ("short_text", "is_active", "created_at")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("text",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Announcement Text", {
            "fields": ("text",),
            "description": (
                "<b>How to write announcements:</b><br><br>"
                "1️⃣ Normal text is white by default.<br>"
                "2️⃣ Use HTML <code>&lt;span&gt;</code> to add colors.<br><br>"

                "<b>Examples:</b><br><br>"

                "👉 Coupon:<br>"
                "<code>Use Code &lt;span style='color:#ffd700;'&gt;SHARKTANK5&lt;/span&gt; "
                "for &lt;span style='color:#00cfff;'&gt;5% OFF&lt;/span&gt;</code><br><br>"

                "👉 Brand:<br>"
                "<code>As Seen On &lt;span style='color:#00cfff;'&gt;SHARK TANK&lt;/span&gt; "
                "&lt;span style='color:#ffd700;'&gt;INDIA&lt;/span&gt;</code><br><br>"

                "⚠️ Do not use &lt;script&gt; or unsafe HTML."
            ),
        }),
        ("Settings", {
            "fields": ("is_active",),
        }),
    )

    def short_text(self, obj):
        return obj.text[:50] + ("…" if len(obj.text) > 50 else "")

    short_text.short_description = "Announcement"


# ------------------------
# HERO SLIDES
# ------------------------

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("id", "preview", "link", "created_at")
    readonly_fields = ("preview",)
    ordering = ("created_at",)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                obj.image.url
            )
        return "—"
    preview.short_description = "Image"


# ------------------------
# CUSTOMER REVIEWS
# ------------------------

@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "is_active", "created_at", "photo_preview")
    list_filter = ("rating", "is_active")
    list_editable = ("is_active",)
    search_fields = ("name", "review")
    readonly_fields = ("photo_preview",)
    ordering = ("-created_at",)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;border-radius:50%;object-fit:cover;" />',
                obj.photo.url
            )
        return "—"
    photo_preview.short_description = "Photo"


# ------------------------
# NEWSLETTER SUBSCRIBERS ✅
# ------------------------

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    search_fields = ("email",)
    ordering = ("-subscribed_at",)

    def has_change_permission(self, request, obj=None):
        return False  # emails should not be edited

    def has_add_permission(self, request):
        return False  # added only via site

    def has_delete_permission(self, request, obj=None):
        return True   # allow cleanup
