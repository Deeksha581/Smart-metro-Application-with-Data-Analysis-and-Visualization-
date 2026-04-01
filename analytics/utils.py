import matplotlib.pyplot as plt
from passengers.models import Passenger
import os
from django.conf import settings

def generate_station_chart():
    stations = {}
    passengers = Passenger.objects.all()

    for p in passengers:
        stations[p.source_station] = stations.get(p.source_station, 0) + 1

    names = list(stations.keys())
    counts = list(stations.values())

    plt.figure(figsize=(8,5))
    plt.bar(names, counts)
    plt.title("Passenger Count per Source Station")
    plt.xlabel("Station")
    plt.ylabel("Passengers")
    plt.tight_layout()

    img_path = os.path.join(settings.STATICFILES_DIRS[0], 'images', 'analytics_chart.png')
    plt.savefig(img_path)
    plt.close()

    return 'images/analytics_chart.png'
