from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import os


class HomePage(models.Model):
    title = models.CharField(max_length=100, default="Home")

    def clean(self):
        if not self.pk and HomePage.objects.exists():
            raise ValidationError("Only one Home Page is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Home Page"


class SiteLogo(models.Model):
    image = models.ImageField(upload_to="site/logo/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # 🔥 DELETE OLD LOGO (HARD REPLACE)
        if not self.pk:
            old = SiteLogo.objects.first()
            if old:
                if old.image and os.path.isfile(old.image.path):
                    os.remove(old.image.path)
                old.delete()

        super().save(*args, **kwargs)

    def __str__(self):
        return "Site Logo"
