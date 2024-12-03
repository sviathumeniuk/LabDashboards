from django.shortcuts import render
from myapp.models import Flight
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
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

def create_bokeh_chart(df):
    if df.empty:
        return None, "<p>Дані для графіка відсутні.</p>"

    source = ColumnDataSource(df)

    p = figure(
        x_range=df['flightnumber'],
        title="Кількість багажу на обраних рейсах",
        toolbar_location="right",
        tools="hover,pan,box_zoom,reset,save",
        width=900,
        height=400,
    )

    p.vbar(
        x='flightnumber',
        top='total_baggage',
        source=source,
        width=0.9,
        color="orange",
        legend_label="Багаж"
    )
    p.xaxis.major_label_orientation = 1.2
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Кількість багажу"
    p.add_tools(HoverTool(tooltips=[("Рейс", "@flightnumber"), ("Кількість багажу", "@total_baggage")]))

    script, div = components(p)
    return script, div

def baggage_by_flight(request):
    selected_flights = request.GET.getlist('flightnumber', [])

    baggage_data = get_baggage_data(selected_flights)
    df_baggage_by_flight = prepare_dataframe(baggage_data)

    stats = calculate_statistics(df_baggage_by_flight)

    script, div = create_bokeh_chart(df_baggage_by_flight)

    all_flights = Flight.objects.values_list('flightnumber', flat=True).distinct()

    return render(request, 'myapp/baggage_per_flight_dash1.html', {
        'script': script,
        'div': div,
        'all_flights': all_flights,
        'selected_flights': selected_flights,
        'stats': stats,
    })
