from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.analytics_dashboard, name="analytics_dashboard"),

    # APIs used by charts
    path("api/station-distribution/", views.station_distribution_api, name="station_distribution_api"),
    path("api/station-average-price/", views.station_vs_avg_price_api, name="station_avg_price_api"),
]
