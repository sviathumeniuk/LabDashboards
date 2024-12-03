from rest_framework import serializers
from .models import Airplane, Flight, Ticket, Passenger, Baggage, Airport, Position, Route, Staff

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset = Route.objects.all())
    airplane = serializers.PrimaryKeyRelatedField(queryset = Airplane.objects.all())
    
    class Meta:
        model = Flight
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    passenger = serializers.PrimaryKeyRelatedField(queryset = Passenger.objects.all())
    flight = serializers.PrimaryKeyRelatedField(queryset = Flight.objects.all())

    class Meta:
        model = Ticket
        fields = '__all__'

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'

class BaggageSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset = Ticket.objects.all())

    class Meta:
        model = Baggage
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    departureairport = serializers.PrimaryKeyRelatedField(queryset = Airport.objects.all())
    arrivalairport = serializers.PrimaryKeyRelatedField(queryset = Airport.objects.all())

    class Meta:
        model = Route
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset = Position.objects.all())
    flight = serializers.PrimaryKeyRelatedField(queryset = Flight.objects.all())

    class Meta:
        model = Staff
        fields = '__all__'