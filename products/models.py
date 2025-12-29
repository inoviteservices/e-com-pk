from django.db import models
from django.utils import timezone

class HeroSlide(models.Model):
    image = models.ImageField(upload_to="hero/")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Hero Slide {self.id}"

    # 🔥 STEP 2 GOES HERE
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        slides = HeroSlide.objects.order_by("created_at")
        if slides.count() > 5:
            for slide in slides[: slides.count() - 5]:
                slide.delete()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    sku = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # new single image field on the same table
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return self.title


