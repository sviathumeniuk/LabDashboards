from django.shortcuts import render
from myapp.models import Route
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from myapp.queries.income_per_flight import get_filtered_routes

def prepare_heatmap_data(queryset):
    routes = list(queryset.values('departure', 'destination', 'total_revenue'))
    df = pd.DataFrame(routes)

    stats = {'mean': 0, 'median': 0, 'min': 0, 'max': 0}  # Значення за замовчуванням

    if not df.empty:
        df = df.groupby(['departure', 'destination'], as_index=False).agg({'total_revenue': 'sum'})
        df_pivot = df.pivot(index='destination', columns='departure', values='total_revenue')
        df_pivot = df_pivot.fillna(0)

        z = df_pivot.values.tolist()
        departures = list(df_pivot.columns)
        destinations = list(df_pivot.index)

        all_revenue = df['total_revenue']
        stats = {
            'mean': all_revenue.mean(),
            'median': all_revenue.median(),
            'min': all_revenue.min(),
            'max': all_revenue.max(),
        }
    else:
        z, departures, destinations = [], [], []

    return z, departures, destinations, stats

def create_plotly_heatmap(z, departures, destinations):
    if not z:
        return "<p>No data available for the selected filters.</p>"

    heatmap = go.Heatmap(
        z=z,
        x=departures,
        y=destinations,
        colorscale='Viridis',
        colorbar=dict(title='Total Revenue'),
        hovertemplate=(
            '<b>Departure:</b> %{x}<br>' +
            '<b>Destination:</b> %{y}<br>' +
            '<b>Total Revenue:</b> %{z:$,.2f}<extra></extra>'
        )
    )

    layout = go.Layout(
        title='Heatmap of Total Revenue per Route',
        xaxis=dict(title='Departure', ticks='', nticks=len(departures)),
        yaxis=dict(title='Destination', ticks='', nticks=len(destinations)),
        autosize=True,
        width=900,
        height=600
    )

    fig = go.Figure(data=[heatmap], layout=layout)
    return pyo.plot(fig, include_plotlyjs=False, output_type='div')

def revenue_heatmap(request):
    selected_departure = request.GET.get('departure', None)
    selected_destination = request.GET.get('destination', None)

    queryset = get_filtered_routes(selected_departure, selected_destination)
    z, departures, destinations, stats = prepare_heatmap_data(queryset)

    all_departures = Route.objects.values_list('departure', flat=True).distinct()
    all_destinations = Route.objects.values_list('destination', flat=True).distinct()

    plot_div = create_plotly_heatmap(z, departures, destinations)

    return render(request, 'myapp/income_per_flight_dash2.html', {
        'plot_div': plot_div,
        'all_departures': all_departures,
        'all_destinations': all_destinations,
        'selected_departure': selected_departure,
        'selected_destination': selected_destination,
        'stats': stats,
    })