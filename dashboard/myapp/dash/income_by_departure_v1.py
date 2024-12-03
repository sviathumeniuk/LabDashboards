from django.shortcuts import render
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from myapp.queries.income_by_departure import get_revenue_data

def prepare_revenue_dataframe(revenue_data, sort_order="default"):
    df = pd.DataFrame(list(revenue_data))
    if not df.empty:
        df = df.groupby('departure', as_index=False).sum()
    else:
        df = pd.DataFrame(columns=['departure', 'total_revenue'])

    if sort_order == "alphabetical":
        df = df.sort_values(by='departure', ascending=True).reset_index(drop=True)
    elif sort_order == "reverse_alphabetical":
        df = df.sort_values(by='departure', ascending=False).reset_index(drop=True)

    return df

def calculate_revenue_statistics(df):
    if df.empty:
        return {
            'mean': 0,
            'median': 0,
            'min': 0,
            'max': 0
        }

    return {
        'mean': np.mean(df['total_revenue']),
        'median': np.median(df['total_revenue']),
        'min': np.min(df['total_revenue']),
        'max': np.max(df['total_revenue'])
    }

def create_revenue_chart(df):
    if df.empty:
        return None, "<p>Немає даних для побудови графіка.</p>"

    source = ColumnDataSource(df)
    unique_departures = df['departure'].astype(str).unique().tolist()

    p = figure(
        x_range=unique_departures,
        title="Загальний дохід за пунктами відправлення",
        x_axis_label="Пункт відправлення",
        y_axis_label="Дохід (грн)",
        width=900,
        height=400,
        tools="hover,pan,box_zoom,reset,save"
    )

    p.line(
        x='departure',
        y='total_revenue',
        source=source,
        line_width=2,
        legend_label="Дохід",
        color="blue"
    )

    p.circle(
        x='departure',
        y='total_revenue',
        source=source,
        size=8,
        color="red",
        legend_label="Дохід"
    )

    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 1.2

    script, div = components(p)
    return script, div

def revenue_by_departure(request):
    sort_order = request.GET.get('sort', 'default')

    revenue_data = get_revenue_data()
    df_revenue = prepare_revenue_dataframe(revenue_data, sort_order)

    stats = calculate_revenue_statistics(df_revenue)
    script, div = create_revenue_chart(df_revenue)

    return render(request, 'myapp/income_by_departure_dash1.html', {
        'script': script,
        'div': div,
        'stats': stats,
        'sort_order': sort_order,
    })