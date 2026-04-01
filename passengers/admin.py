from django.contrib import admin
from .models import Passenger
from .utils import most_traveled_routes

class PassengerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'age',
        'gender',
        'source_station',
        'destination_station',
        'travel_date',
        'ticket_price'
    )

    change_list_template = "admin/passengers/passenger_changelist.html"

    def changelist_view(self, request, extra_context=None):
        labels, values = most_traveled_routes()

        extra_context = extra_context or {}
        extra_context['route_labels'] = labels
        extra_context['route_values'] = values

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Passenger, PassengerAdmin)
