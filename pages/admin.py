from django.contrib import admin
from .models import HomePage, SiteLogo


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not HomePage.objects.exists()


@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteLogo.objects.exists()
