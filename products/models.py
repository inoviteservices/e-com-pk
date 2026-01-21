from django.db import models
from django.utils import timezone


from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        help_text="Image shown on homepage & category cards"
    )

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

     # 🔥 NEW FLAG
    requires_custom_image = models.BooleanField(default=False)

    def __str__(self):
        return self.title


