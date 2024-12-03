from django.db.models import Count
from myapp.models import Flight

def get_baggage_data(selected_flights):
    baggage_data = Flight.objects.annotate(
        total_baggage=Count('ticket__baggage')
    ).filter(total_baggage__gt=0)

    if selected_flights and 'all' not in selected_flights:
        baggage_data = baggage_data.filter(flightnumber__in=selected_flights)

    return baggage_data.order_by('-total_baggage')

