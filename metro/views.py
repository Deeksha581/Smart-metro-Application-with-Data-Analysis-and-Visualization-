from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import MetroCard, UserProfile

def home(request):
    return render(request, 'common/home.html')

def metro_stations(request):
    return render(request, 'metro/stations.html')

def safety(request):
    return render(request, 'metro/safety.html')

def payment(request):
    return render(request, 'metro/payment.html')

@login_required
def token_ticket(request):
    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        pay_app = request.POST.get("pay_app")

        # Demo fare (can be enhanced later)
        fare = 40

        context = {
            "source": source,
            "destination": destination,
            "fare": fare,
            "pay_app": pay_app,
        }
        return render(request, "metro/token_pay.html", context)

    return render(request, "metro/token_ticket.html")

@login_required
def metro_card(request):
    profile = UserProfile.objects.filter(email=request.user.email).first()
    card = MetroCard.objects.filter(user_profile=profile).first() if profile else None

    return render(request, "metro/metro_card.html", {"card": card})

def online_payment(request):
    return render(request, "metro/online_payment.html")

def fare_check(request):
    return render(request, "metro/fare_check.html")

def pass_system(request):
    return render(request, "metro/pass_system.html")

def about(request):
    return render(request, "metro/about.html")
def metro_map(request):
    return render(request, "metro/map.html")
