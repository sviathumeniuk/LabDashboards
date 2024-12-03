from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
from django.db import connection
import time
import pandas as pd
import plotly.express as px
from plotly.offline import plot

def get_flight_query():
    return """
        SELECT
            Flight.FlightNumber AS FlightNumber,
            Flight.DepartureTime AS DepartureTime,
            Flight.ArrivalTime AS ArrivalTime,
            Airplane.Model AS AirplaneModel,
            Route.RouteID AS RouteID,
            DepartureAirport.Name AS DepartureAirport,
            ArrivalAirport.Name AS ArrivalAirport,
            Staff.name AS StaffName,
            Position.positionname AS PositionName
        FROM Flight
        JOIN Airplane ON Flight.AirplaneID = Airplane.airplaneid
        JOIN Route ON Flight.RouteID = Route.routeid
        JOIN Airport AS DepartureAirport ON Route.DepartureAirportID = DepartureAirport.airportid
        JOIN Airport AS ArrivalAirport ON Route.ArrivalAirportID = ArrivalAirport.airportid
        LEFT JOIN Staff ON Flight.FlightID = Staff.flightid
        LEFT JOIN Position ON Staff.positionname = Position.positionname
    """

def execute_query(query=None, params=None):
    query = query or get_flight_query()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def threaded_query_execution(queries, max_threads=12):
    results = []
    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(execute_query, query) for query in queries]
        for future in futures:
            results.append(future.result())
    return results

def measure_performance(queries, mode='thread', params_range=[2, 4, 6, 8, 10]):
    results = []
    for param in params_range:
        start_time = time.time()
        if mode == 'thread':
            threaded_query_execution(queries, max_threads=param)
        end_time = time.time()
        results.append({
            'mode': mode,
            'parameter': param,
            'execution_time': end_time - start_time
        })
    return results

def performance_chart(request):
    queries = [get_flight_query() for _ in range(200)]

    thread_results = measure_performance(queries, mode='thread')

    results_df = pd.DataFrame(thread_results)

    fig = px.line(
        results_df,
        x='parameter',
        y='execution_time',
        title='Performance of Threading vs Multiprocessing',
        labels={'parameter': 'Number of Threads', 'execution_time': 'Execution Time (s)'}
    )

    graph_html = plot(fig, output_type='div')

    return render(request, 'myapp/experiment_dashboard.html', {'graph_html': graph_html})