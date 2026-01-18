from django.db import models



class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Art Gift")
    logo = models.ImageField(upload_to="branding/")
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True)

    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name_plural = "Site Settings"
class AnalyticsSettings(models.Model):
    ga4_measurement_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Example: G-XXXXXXXXXX"
    )
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "Analytics Settings"
