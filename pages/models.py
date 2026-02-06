from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import os


class SiteLogo(models.Model):
    image = models.ImageField(upload_to="site/logo/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # HARD REPLACE: only one logo allowed
        if not self.pk:
            old = SiteLogo.objects.first()
            if old:
                if old.image and os.path.isfile(old.image.path):
                    os.remove(old.image.path)
                old.delete()

        super().save(*args, **kwargs)

    def __str__(self):
        return "Site Logo"


class SiteAnnouncement(models.Model):
    text = models.CharField(
        max_length=255,
        help_text=(
            "You can use simple HTML to add colors. "
            "Example: "
            "Use Code <span style='color:#ffd700;'>SHARKTANK5</span> "
            "for <span style='color:#00cfff;'>5% OFF</span>"
        )
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    MAX_ANNOUNCEMENTS = 5

    def clean(self):
        # Allow update, block only new if limit reached
        if not self.pk:
            count = SiteAnnouncement.objects.count()
            if count >= self.MAX_ANNOUNCEMENTS:
                raise ValidationError(
                    f"Maximum {self.MAX_ANNOUNCEMENTS} announcements allowed."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:40]
    


class HeroSlide(models.Model):
    image = models.ImageField(upload_to="site/hero/")
    link = models.CharField(
        max_length=255,
        help_text="URL or product path (e.g. /products/wooden-frame/)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    MAX_SLIDES = 3

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 🔥 Enforce FIFO: keep only latest 3 slides
        slides = HeroSlide.objects.order_by("created_at")
        if slides.count() > self.MAX_SLIDES:
            excess = slides.count() - self.MAX_SLIDES
            for slide in slides[:excess]:
                if slide.image and os.path.isfile(slide.image.path):
                    os.remove(slide.image.path)
                slide.delete()

    def __str__(self):
        return f"Hero Slide {self.id}"

def validate_image_size(image):
    max_size_mb = 1  # 1 MB max
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError("Image size should not exceed 1 MB.")


class CustomerReview(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Customer name"
    )

    photo = models.ImageField(
        upload_to="reviews/",
        validators=[validate_image_size],
        blank=True,
        null=True,
        help_text="Small square image recommended (e.g. 200x200px)"
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

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.rating}★)"
    

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email