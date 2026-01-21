from .models import SiteLogo, SiteAnnouncement, HeroSlide


def site_globals(request):
    announcement = SiteAnnouncement.objects.filter(is_active=True).first()
    logo = SiteLogo.objects.first()

    slides_qs = HeroSlide.objects.order_by("created_at")
    has_custom_slides = slides_qs.exists()

    return {
        "site_announcement": announcement,
        "site_logo": logo,
        "hero_slides": slides_qs,
        "has_custom_slides": has_custom_slides,
    }
