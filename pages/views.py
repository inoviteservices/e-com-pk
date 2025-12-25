from django.shortcuts import render

def terms_of_service(request):
    return render(request, "pages/terms-of-service.html")

def shipping_policy(request):
    return render(request, "pages/shipping-policy.html")

def return_policy(request):
    return render(request, "pages/return-policy.html")

def privacy_policy(request):
    return render(request, "pages/privacy-policy.html")
