from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator



class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True, blank=True)

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        help_text="Image shown on homepage & category cards"
    )


    def save(self, *args, **kwargs):

        # Auto-generate slug from name
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name



class Product(models.Model):

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    compare_at_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    sku = models.CharField(max_length=100, unique=True, blank=True)

    stock = models.IntegerField()

    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True
    )

    requires_custom_image = models.BooleanField(default=False)


    def save(self, *args, **kwargs):

        # Auto-generate slug from title
        if not self.slug:
            self.slug = slugify(self.title)

        # Auto-generate sku from title
        if not self.sku:
            self.sku = slugify(self.title)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

class HotSingle(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="hot_single"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return f"Hot: {self.product.title}"


class CustomerReview(models.Model):

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Product this review belongs to"
    )

    name = models.CharField(
        max_length=100,
        help_text="Customer name"
    )

    

    review = models.TextField(
        max_length=500,
        help_text="Customer review (max 500 characters)"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        help_text="Rating from 1 to 5"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this review"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.title} – {self.name} ({self.rating}★)"