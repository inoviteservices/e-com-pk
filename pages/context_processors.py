from .models import SiteLogo


def site_logo(request):
    logo = SiteLogo.objects.first()
    return {
        "site_logo": logo.image.url if logo else "/static/images/logo.png"
    }
