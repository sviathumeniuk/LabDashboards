from myapp.models import Staff
import pandas as pd


def get_staff_data(flight_id, min_salary):
    query = Staff.objects.filter(flight_id=flight_id)
    if min_salary:
        query = query.filter(position__salary__gte=min_salary)
    return pd.DataFrame(list(query.select_related('position').values(
        'name', 'position__positionname', 'position__salary'
    )))