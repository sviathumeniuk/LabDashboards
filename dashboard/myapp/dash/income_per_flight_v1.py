from django.shortcuts import render
from django.db.models import Sum, Count
from myapp.models import Route
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar
from myapp.queries.income_per_flight import get_filtered_routes

def prepare_heatmap_data(queryset):
    df = pd.DataFrame(list(queryset.values('departure', 'destination', 'total_revenue')))
    if df.empty:
        return pd.DataFrame(columns=['departure', 'destination', 'total_revenue'])
    
    df = df.groupby(['departure', 'destination'], as_index=False).agg({'total_revenue': 'sum'})
    df_pivot = df.pivot(index='destination', columns='departure', values='total_revenue')
    df_melted = df_pivot.reset_index().melt(id_vars='destination', var_name='departure', value_name='total_revenue')
    df_melted.dropna(subset=['total_revenue'], inplace=True)
    
    stats = {
        'mean': df_melted['total_revenue'].mean(),
        'median': df_melted['total_revenue'].median(),
        'min': df_melted['total_revenue'].min(),
        'max': df_melted['total_revenue'].max(),
    }
    
    return df_melted, stats

def create_heatmap(df_melted, departures, destinations):
    source = ColumnDataSource(df_melted)
    p = figure(
        title="Heatmap of Total Revenue per Route",
        x_range=list(departures),
        y_range=list(destinations),
        x_axis_location="above",
        width=900,
        height=600,
        tools="hover,save,pan,box_zoom,reset,wheel_zoom",
        toolbar_location='below',
        tooltips=[('Departure', '@departure'), ('Destination', '@destination'), ('Total Revenue', '@total_revenue{0,0}')],
    )
    if not df_melted.empty:
        mapper = LinearColorMapper(palette='Viridis256', low=df_melted['total_revenue'].min(), high=df_melted['total_revenue'].max())
        p.rect(x="departure", y="destination", width=1, height=1, source=source, fill_color={'field': 'total_revenue', 'transform': mapper}, line_color=None)
        color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
        p.add_layout(color_bar, 'right')
        
        p.xaxis.major_label_orientation = "vertical"
        p.xaxis.major_label_text_font_size = "8pt"
        p.yaxis.major_label_text_font_size = "8pt"

    return components(p)

def revenue_heatmap(request):
    selected_departure = request.GET.get('departure', None)
    selected_destination = request.GET.get('destination', None)
    
    queryset = get_filtered_routes(selected_departure, selected_destination)
    
    df_melted, stats = prepare_heatmap_data(queryset)
    
    departures = Route.objects.values_list('departure', flat=True).distinct()
    destinations = Route.objects.values_list('destination', flat=True).distinct()
    
    script, div = create_heatmap(df_melted, departures, destinations)
    
    return render(request, 'myapp/income_per_flight_dash1.html', {
        'script': script,
        'div': div,
        'departures': departures,
        'destinations': destinations,
        'selected_departure': selected_departure,
        'selected_destination': selected_destination,
        'stats': stats,
    })
