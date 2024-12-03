from django.db import models

class Airplane(models.Model):
    airplaneid = models.AutoField(primary_key = True)
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    manufacturer = models.CharField(max_length = 50)

    class Meta:
        db_table = 'airplane'

class Airport(models.Model):
    airportid = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    city = models.CharField(max_length = 30)
    country = models.CharField(max_length = 3)

    class Meta:
        db_table = 'airport'

class Baggage(models.Model):
    baggageid = models.AutoField(primary_key = True)
    weight = models.DecimalField(max_digits = 5, decimal_places = 2)
    ticket = models.ForeignKey('Ticket', on_delete = models.CASCADE, db_column = 'ticketid')

    class Meta:
        db_table = 'baggage'

class Flight(models.Model):
    flightid = models.AutoField(primary_key = True)
    flightnumber = models.CharField(max_length = 10)
    departuretime = models.DateTimeField()
    arrivaltime = models.DateTimeField()
    airplane = models.ForeignKey('Airplane', on_delete = models.CASCADE, db_column = 'AirplaneID')
    route = models.ForeignKey('Route', on_delete = models.CASCADE, db_column = 'RouteID')

    class Meta:
        db_table = 'flight'

class Passenger(models.Model):
    passengerid = models.AutoField(primary_key = True)
    name = models.TextField()
    email = models.EmailField(max_length = 50)
    passportnumber = models.CharField(max_length = 15)

    class Meta:
        db_table = 'passenger'

class Position(models.Model):
    positionname = models.CharField(max_length = 45, primary_key = True)
    salary = models.IntegerField()

    class Meta:
        db_table = 'position'

class Route(models.Model):
    routeid = models.AutoField(primary_key = True)
    departure = models.CharField(max_length = 50)
    destination = models.CharField(max_length = 50)
    duration = models.TimeField()
    departureairport = models.ForeignKey('Airport', on_delete = models.CASCADE, db_column = 'DepartureAirportID', related_name = 'departure_routes')
    arrivalairport = models.ForeignKey('Airport', on_delete = models.CASCADE, db_column = 'ArrivalAirportID', related_name = 'arrival_routes')

    class Meta:
        db_table = 'route'

class Staff(models.Model):
    staffid = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 55)
    flight = models.ForeignKey('Flight', on_delete = models.CASCADE, db_column = 'flightid')
    position = models.ForeignKey('Position', on_delete = models.CASCADE, db_column = 'positionname')  # Додаємо зв'язок з посадою

    class Meta:
        db_table = 'staff'
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'

class Ticket(models.Model):
    ticketid = models.AutoField(primary_key = True)
    price = models.IntegerField()
    seatnumber = models.IntegerField()
    passenger = models.ForeignKey('Passenger', on_delete = models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete = models.CASCADE)

    class Meta:
        db_table = 'ticket'