from django.db.models import Count, F
from myapp.models import Airplane

def get_airplane_data():
    return Airplane.objects.annotate(
        total_seats=F('capacity'),
        total_tickets_sold=Count('flight__ticket')
    ).filter(total_tickets_sold__gt=0)
