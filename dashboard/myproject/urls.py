from django.contrib import admin
from django.urls import path
from myapp.dash import (
    tickets_on_flight_v1, tickets_on_flight_v2, experiment, airplane_load_v1, airplane_load_v2,
    income_by_departure_v1, income_by_departure_v2, baggage_per_flight_v1, baggage_per_flight_v2,
    staff_on_flight_v1, staff_on_flight_v2, income_per_flight_v1, income_per_flight_v2
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('staff-on-flight/v1/<int:flight_id>/', staff_on_flight_v1.staff_on_flight_dash1, name='staff_on_flight_v1'),
    path('staff-on-flight/v2/<int:flight_id>/', staff_on_flight_v2.staff_on_flight_dash2, name='staff_on_flight_v2'),

    path('tickets-on-flight/v1/<int:flight_id>/', tickets_on_flight_v1.tickets_on_flight_dash1, name='tickets_on_flight_v1'),
    path('tickets-on-flight/v2/<int:flight_id>/', tickets_on_flight_v2.tickets_on_flight_dash2, name='tickets_on_flight_v2'),

    path('income-per-flight/v1/', income_per_flight_v1.revenue_heatmap, name='income_per_flight_v1'),
    path('income-per-flight/v2/', income_per_flight_v2.revenue_heatmap, name='income_per_flight_v2'),

    path('baggage-per-flight/v1/', baggage_per_flight_v1.baggage_by_flight, name='baggage_per_flight_v1'),
    path('baggage-per-flight/v2/', baggage_per_flight_v2.baggage_by_flight, name='baggage_per_flight_v2'),

    path('airplane-load/v1/', airplane_load_v1.airplane_load_analysis, name='airplane_load_v1'),
    path('airplane-load/v2/', airplane_load_v2.airplane_load_analysis, name='airplane_load_v2'),

    path('income-by-departure/v1/', income_by_departure_v1.revenue_by_departure, name='income_by_departure_v1'),
    path('income-by-departure/v2/', income_by_departure_v2.revenue_by_departure, name='income_by_departure_v2'),

    path('experiment/', experiment.performance_chart, name='experiment'),
]
