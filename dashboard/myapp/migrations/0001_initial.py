# Generated by Django 5.0 on 2024-10-12 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('airplaneid', models.AutoField(primary_key=True, serialize=False)),
                ('model', models.CharField(blank=True, max_length=100, null=True)),
                ('capacity', models.IntegerField()),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'airplane',
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('airportid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('country', models.CharField(blank=True, max_length=3, null=True)),
            ],
            options={
                'db_table': 'airport',
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('passengerid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('passportnumber', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'passenger',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('positionid', models.AutoField(primary_key=True, serialize=False)),
                ('positionname', models.CharField(max_length=45)),
                ('salary', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'position',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('routeid', models.AutoField(primary_key=True, serialize=False)),
                ('departure', models.CharField(blank=True, max_length=50, null=True)),
                ('destination', models.CharField(blank=True, max_length=50, null=True)),
                ('duration', models.TimeField(blank=True, null=True)),
                ('arrivalairportid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_airport', to='myapp.airport')),
                ('departureairportid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_airport', to='myapp.airport')),
            ],
            options={
                'db_table': 'route',
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flightid', models.AutoField(primary_key=True, serialize=False)),
                ('flightnumber', models.CharField(max_length=10)),
                ('departuretime', models.DateTimeField()),
                ('arrivaltime', models.DateTimeField()),
                ('airplaneid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.airplane')),
                ('routeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.route')),
            ],
            options={
                'db_table': 'flight',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staffid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('flightid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.flight')),
                ('positionid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.position')),
            ],
            options={
                'db_table': 'staff',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticketid', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.IntegerField()),
                ('seatnumber', models.IntegerField()),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.flight')),
                ('passenger_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.passenger')),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='Baggage',
            fields=[
                ('baggageid', models.AutoField(primary_key=True, serialize=False)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ticketid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.ticket')),
            ],
            options={
                'db_table': 'baggage',
            },
        ),
    ]
