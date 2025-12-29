from django.contrib import admin
from .models import HeroSlide,Product, Category

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")

    
admin.site.register(Product)
admin.site.register(Category)
