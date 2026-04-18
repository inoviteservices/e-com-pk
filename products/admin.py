from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Product, Category, CustomerReview, HotSingle, ProductImage, ProductVideo, ProductVariant
import csv
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from io import TextIOWrapper


# ------------------------
#  INLINE (CLEAN + USABLE)
# ------------------------

class CustomerReviewInline(admin.TabularInline):
    model = CustomerReview
    extra = 0
    can_delete = True
    show_change_link = True

    fields = (
        "name",
        "rating",
        "review",
        "media",
        "is_active",
        "created_at",
    )

    readonly_fields = ("created_at",)

    # 🔥 Make review textarea compact (fixes ugly UI)
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={
                "rows": 3,
                "cols": 40,
                "style": "resize:vertical;"
            })
        }
    }

class ProductImageInline(admin.TabularInline):

    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    can_delete = True
    show_change_link = True

class ProductVideoInline(admin.TabularInline):

    model = ProductVideo
    extra = 0
    min_num = 0
    can_delete = True
    show_change_link = True


# ------------------------
# PRODUCT ADMIN
# ------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = [ProductImageInline,ProductVideoInline,ProductVariantInline]

    list_display = (
        "title",
        "price",
        "stock",
        "sold_units",
        "is_active",
    )

    list_editable = (
        "stock",
        "sold_units",
        "is_active",
    )

    exclude = ("slug", "sku")

    search_fields = ("title", "sku")

    list_filter = ("is_active", "category")


# ------------------------
# Hot Single
# ------------------------

@admin.register(HotSingle)
class HotSingleAdmin(admin.ModelAdmin):

    list_display = ("product", "is_active", "created_at")

    list_editable = ("is_active",)

    list_filter = ("is_active",)

    search_fields = ("product__title",)

    ordering = ("-created_at",)

# ------------------------
# CATEGORY ADMIN
# ------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name",)
    exclude = ("slug",)


# ------------------------
# REVIEW ADMIN (OPTIONAL BUT VERY USEFUL)
# ------------------------
@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "name",
        "rating",
        "media_preview",
        "is_active",
        "created_at",
    )
    def media_preview(self, obj):
        from django.utils.html import format_html

        if obj.media:
            url = obj.media.url.lower()

            if url.endswith((".mp4", ".webm", ".mov")):
                return format_html(
                    '<video width="80" controls><source src="{}"></video>',
                    obj.media.url
                )
            else:
                return format_html(
                    '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;">',
                    obj.media.url
                )

        return "No Media"

    media_preview.short_description = "Media"

    list_filter = (
        "rating",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "review",
        "product__title",
    )

    readonly_fields = ("created_at",)

    actions = ["export_as_csv"]

    change_list_template = "admin/reviews_changelist.html"

    # ✅ PAGINATION (SHOW ONLY 6 PER PAGE)
    list_per_page = 6


    # ------------------------
    # EXPORT CSV
    # ------------------------
    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="reviews.csv"'

        writer = csv.writer(response)

        writer.writerow([
            "product_slug",
            "name",
            "rating",
            "review",
            "is_active",
        ])

        for review in queryset:
            writer.writerow([
                review.product.slug,
                review.name,
                review.rating,
                review.review,
                review.is_active,
            ])

        return response


    export_as_csv.short_description = "Export Selected as CSV"


    # ------------------------
    # IMPORT CSV
    # ------------------------
    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "import-csv/",
                self.import_csv,
                name="reviews_import_csv",
            ),
        ]

        return custom_urls + urls


    def import_csv(self, request):

        if request.method == "POST":

            csv_file = request.FILES.get("csv_file")

            if not csv_file:
                messages.error(request, "No file uploaded.")
                return redirect("..")

            if not csv_file.name.endswith(".csv"):
                messages.error(request, "File must be CSV.")
                return redirect("..")


            file_data = TextIOWrapper(
                csv_file.file,
                encoding="utf-8"
            )

            reader = csv.DictReader(file_data)

            created_count = 0


            for row in reader:

                try:

                    product = Product.objects.get(
                        slug=row["product_slug"]
                    )

                    CustomerReview.objects.create(
                        product=product,
                        name=row["name"],
                        rating=int(row["rating"]),
                        review=row["review"],
                        is_active=row["is_active"].lower() == "true",
                    )

                    created_count += 1


                except Exception as e:

                    continue


            messages.success(
                request,
                f"{created_count} reviews imported successfully."
            )

            return redirect("..")


        return render(
            request,
            "admin/import_reviews_csv.html"
        )

