from django.db.models import Sum, Count
from myapp.models import Route

def get_filtered_routes(selected_departure, selected_destination):
    queryset = Route.objects.annotate(
        total_revenue=Sum('flight__ticket__price'),
        flight_count=Count('flight')
    ).filter(total_revenue__gt=0).order_by('-total_revenue')

    if selected_departure and selected_departure != "All":
        queryset = queryset.filter(departure=selected_departure)
    if selected_destination and selected_destination != "All":
        queryset = queryset.filter(destination=selected_destination)
    
    return queryset
