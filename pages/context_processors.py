from .models import SiteLogo, SiteAnnouncement, HeroSlide


def site_globals(request):

    announcements = SiteAnnouncement.objects.filter(
        is_active=True
    ).order_by("-created_at")[:5]   # Max 5 latest active

    logo = SiteLogo.objects.first()

    slides_qs = HeroSlide.objects.order_by("created_at")
    has_custom_slides = slides_qs.exists()

    return {
        "site_announcements": announcements,  # plural
        "site_logo": logo,
        "hero_slides": slides_qs,
        "has_custom_slides": has_custom_slides,
        
    }
