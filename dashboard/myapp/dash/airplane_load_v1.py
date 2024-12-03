from django.shortcuts import render
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from myapp.queries.airplane_load import get_airplane_data

def prepare_dataframe(data, sort_order):
    df = pd.DataFrame(data)

    if not df.empty:
        df['load_percentage'] = (df['total_tickets_sold'] / df['total_seats']) * 100
        df['model_with_index'] = df['model'] + " #" + df.groupby('model').cumcount().astype(str)

        if sort_order == "asc":
            df = df.sort_values(by='load_percentage', ascending=True).reset_index(drop=True)
        elif sort_order == "desc":
            df = df.sort_values(by='load_percentage', ascending=False).reset_index(drop=True)

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
        'mean': df['load_percentage'].mean(),
        'median': df['load_percentage'].median(),
        'min': df['load_percentage'].min(),
        'max': df['load_percentage'].max()
    }

def create_bokeh_chart(df):
    if df.empty:
        return None, "<p>Дані для графіка відсутні.</p>"

    source = ColumnDataSource(df)

    p = figure(
        x_range=df['model_with_index'].tolist(),
        title="Аналіз завантаження літаків",
        x_axis_label="Модель літака",
        y_axis_label="Завантаження (%)",
        width=900,
        height=500,
        tools="hover,pan,box_zoom,reset,save"
    )

    p.vbar(
        x='model_with_index',
        top='load_percentage',
        width=0.9,
        source=source,
        color="blue",
        legend_label="Завантаження"
    )

    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 1.2

    script, div = components(p)
    return script, div

def airplane_load_analysis(request):
    sort_order = request.GET.get('sort', 'desc')

    airplane_load_data = get_airplane_data()
    data = list(airplane_load_data.values('model', 'manufacturer', 'total_seats', 'total_tickets_sold'))

    df_airplane_load = prepare_dataframe(data, sort_order)

    stats = calculate_statistics(df_airplane_load)
    script, div = create_bokeh_chart(df_airplane_load)

    return render(request, 'myapp/airplane_load_dash1.html', {
        'script': script,
        'div': div,
        'data_table': df_airplane_load.to_dict(orient='records'),
        'stats': stats,
        'sort_order': sort_order,
    })