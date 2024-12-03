from django.shortcuts import render
from myapp.models import Flight
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from myapp.queries.baggage_per_flight import get_baggage_data

def prepare_dataframe(baggage_data):
    df = pd.DataFrame(list(baggage_data.values('flightnumber', 'total_baggage')))
    if df.empty:
        df = pd.DataFrame(columns=['flightnumber', 'total_baggage'])
    return df

def calculate_statistics(df):
    if df.empty:
        return {
            'mean': 0,
            'median': 0,
            'min': 0,
            'max': 0
        }
    
    return {
        'mean': df['total_baggage'].mean(),
        'median': df['total_baggage'].median(),
        'min': df['total_baggage'].min(),
        'max': df['total_baggage'].max()
    }

def create_plotly_chart(df):
    if df.empty:
        return "<p>Дані для графіка відсутні.</p>"

    flight_numbers = df['flightnumber']
    total_baggage = df['total_baggage']

    bar_chart = go.Bar(
        x=flight_numbers,
        y=total_baggage,
        marker=dict(color='orange'),
        text=total_baggage,
        textposition='auto',
        name='Багаж'
    )

    layout = go.Layout(
        title="Кількість багажу на обраних рейсах",
        xaxis=dict(title="Номер рейсу"),
        yaxis=dict(title="Кількість багажу"),
        height=500,
        width=900
    )

    fig = go.Figure(data=[bar_chart], layout=layout)

    return pyo.plot(fig, output_type='div', include_plotlyjs=False)

def baggage_by_flight(request):
    selected_flights = request.GET.getlist('flightnumber', [])

    baggage_data = get_baggage_data(selected_flights)
    df_baggage_by_flight = prepare_dataframe(baggage_data)

    stats = calculate_statistics(df_baggage_by_flight)

    plot_div = create_plotly_chart(df_baggage_by_flight)

    all_flights = Flight.objects.values_list('flightnumber', flat=True).distinct()

    return render(request, 'myapp/baggage_per_flight_dash2.html', {
        'plot_div': plot_div,
        'all_flights': all_flights,
        'selected_flights': selected_flights,
        'stats': stats,
    })