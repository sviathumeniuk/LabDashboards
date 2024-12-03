from django.shortcuts import render
import pandas as pd
import plotly.graph_objects as go
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

def create_plotly_chart(df):
    if df.empty:
        return "<p>Дані для графіка відсутні.</p>"

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df['model_with_index'],
            y=df['load_percentage'],
            marker=dict(color="blue"),
            name="Завантаження",
        )
    )

    fig.update_layout(
        title="Аналіз завантаження літаків",
        xaxis=dict(title="Модель літака", tickangle=-45),
        yaxis=dict(title="Завантаження (%)"),
        height=500,
        width=900,
        template="plotly_white",
    )

    return fig.to_html(full_html=False)

def airplane_load_analysis(request):
    sort_order = request.GET.get('sort', 'default')

    airplane_load_data = get_airplane_data()
    data = list(airplane_load_data.values('model', 'manufacturer', 'total_seats', 'total_tickets_sold'))

    if sort_order == "default":
        df_airplane_load = pd.DataFrame(data)
        if not df_airplane_load.empty:
            df_airplane_load['load_percentage'] = (df_airplane_load['total_tickets_sold'] / df_airplane_load['total_seats']) * 100
            df_airplane_load['model_with_index'] = df_airplane_load['model'] + " #" + df_airplane_load.groupby('model').cumcount().astype(str)
    else:
        df_airplane_load = prepare_dataframe(data, sort_order)

    stats = calculate_statistics(df_airplane_load)
    chart_html = create_plotly_chart(df_airplane_load)

    return render(request, 'myapp/airplane_load_dash2.html', {
        'chart_html': chart_html,
        'data_table': df_airplane_load.to_dict(orient='records'),
        'stats': stats,
        'sort_order': sort_order,
    })
