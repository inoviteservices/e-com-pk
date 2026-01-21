from django.contrib import admin
from django.utils.html import format_html

from .models import (
    SiteLogo,
    SiteAnnouncement,
    HeroSlide,
    CustomerReview,
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
