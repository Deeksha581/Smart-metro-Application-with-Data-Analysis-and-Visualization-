from django.urls import path
from . import views

app_name = "metro"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("stations/", views.metro_stations, name="metro_stations"),
    path("safety/", views.safety, name="safety"),
    path("payment/", views.payment, name="payment"),
    path("token/", views.token_ticket, name="token_ticket"),
    path("card/", views.metro_card, name="metro_card"),
    path("online/", views.online_payment, name="online_payment"),
    path("fare/", views.fare_check, name="fare_check"),
    path("pass/", views.pass_system, name="pass_system"),
    path("map/", views.metro_map, name="metro_map"),
]
