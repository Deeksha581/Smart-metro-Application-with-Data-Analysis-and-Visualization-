from collections import Counter
from .models import Passenger

def most_traveled_routes():
    routes = Passenger.objects.values_list(
        'source_station', 'destination_station'
    )

    route_counts = Counter(routes)

    # Convert to readable format
    labels = [f"{s} → {d}" for s, d in route_counts.keys()]
    values = list(route_counts.values())

    return labels, values
