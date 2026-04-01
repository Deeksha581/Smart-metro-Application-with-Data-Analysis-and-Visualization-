from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg, Min, Max, StdDev
from django.contrib.auth.models import User

from passengers.models import Passenger


# =====================================================
# ADMIN ANALYTICS DASHBOARD (KPIs)
# =====================================================
def analytics_dashboard(request):
    context = {
        "total_users": User.objects.count(),
        "total_records": Passenger.objects.count(),
        "total_tickets": Passenger.objects.count(),
        "total_revenue": Passenger.objects.aggregate(
            total=Avg("ticket_price")
        )["total"] or 0,
    }
    return render(request, "analytics/index.html", context)


# =====================================================
# UNIVARIATE ANALYSIS (BAR CHART API)
# =====================================================
def station_distribution_api(request):
    qs = (
        Passenger.objects
        .values("source_station")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    return JsonResponse({
        "labels": [q["source_station"] for q in qs],
        "values": [q["count"] for q in qs],
    })


# =====================================================
# BIVARIATE ANALYSIS (AVG PRICE API)
# =====================================================
def station_vs_avg_price_api(request):
    qs = (
        Passenger.objects
        .values("source_station")
        .annotate(avg_price=Avg("ticket_price"))
        .order_by("-avg_price")
    )

    return JsonResponse({
        "labels": [q["source_station"] for q in qs],
        "values": [round(q["avg_price"], 2) if q["avg_price"] else 0 for q in qs],
    })


# =====================================================
# LIVE EDA – TASK EXECUTION (TABLE FORMAT)
# =====================================================
def eda_tables(request):
    qs = Passenger.objects.all()

    # 1️⃣ Data Observation & Understanding
    data_observation = {
        "total_rows": qs.count(),
        "total_columns": len(Passenger._meta.fields),
        "columns": [f.name for f in Passenger._meta.fields],
    }

    # 2️⃣ Data Cleaning
    data_cleaning = {
        "missing_source_station": qs.filter(source_station__isnull=True).count(),
        "missing_destination_station": qs.filter(destination_station__isnull=True).count(),
        "duplicate_records": (
            qs.values(
                "name",
                "source_station",
                "destination_station",
                "travel_date"
            )
            .annotate(c=Count("id"))
            .filter(c__gt=1)
            .count()
        ),
    }

    # 3️⃣ Univariate – Categorical
    categorical_counts = (
        qs.values("source_station")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # 4️⃣ Univariate – Numerical
    numerical_stats = qs.aggregate(
        mean_price=Avg("ticket_price"),
        min_price=Min("ticket_price"),
        max_price=Max("ticket_price"),
        std_price=StdDev("ticket_price"),
    )

    # 5️⃣ Bivariate / Grouped Analysis
    grouped_analysis = (
        qs.values("source_station")
        .annotate(avg_price=Avg("ticket_price"))
        .order_by("-avg_price")
    )

    context = {
        "data_observation": data_observation,
        "data_cleaning": data_cleaning,
        "categorical_counts": categorical_counts,
        "numerical_stats": numerical_stats,
        "grouped_analysis": grouped_analysis,
    }

    return render(request, "analytics/eda_tables.html", context)
