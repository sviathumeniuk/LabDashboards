from django.db.models import Sum
from myapp.models import Route

def get_revenue_data():
    revenue_data = Route.objects.annotate(
        total_revenue=Sum('flight__ticket__price')
    ).filter(total_revenue__gt=0).values('departure', 'total_revenue')
    return revenue_data