from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Product, Category, CustomerReview
import csv
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from io import TextIOWrapper


# ------------------------
# REVIEW INLINE (CLEAN + USABLE)
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


# ------------------------
# PRODUCT ADMIN
# ------------------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "price",
        "stock",
        "is_active",
    )

    exclude = ("slug", "sku")

    inlines = [CustomerReviewInline]

    


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
        "is_active",
        "created_at",
    )

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
