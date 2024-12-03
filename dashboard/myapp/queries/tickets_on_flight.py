from ..models import Ticket
import pandas as pd

def get_ticket_data1(flight_id, sort_order='asc'):
    query = Ticket.objects.filter(flight_id=flight_id).select_related('passenger')
    query = query.order_by('-price' if sort_order == 'desc' else 'price')
    return pd.DataFrame(list(query.values('passenger__name', 'price', 'seatnumber')))

def get_ticket_data2(flight_id):
    return pd.DataFrame(list(
        Ticket.objects.filter(flight_id=flight_id)
        .select_related('passenger')
        .order_by('passenger__name')
        .values('passenger__name', 'price', 'seatnumber')
    ))