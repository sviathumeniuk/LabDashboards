from django.contrib import admin
from .models import Airplane, Airport, Baggage, Flight, Passenger, Position, Route, Staff, Ticket

admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Baggage)
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Position)
admin.site.register(Route)
admin.site.register(Staff)
admin.site.register(Ticket)