from django.shortcuts import render
import numpy as np
import pandas as pd
import plotly.graph_objs as go
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
        return "<p>Немає даних для побудови графіка.</p>"

    fig = go.Figure()

    # Add line plot
    fig.add_trace(go.Scatter(
        x=df['departure'],
        y=df['total_revenue'],
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(size=8, color='red'),
        name='Дохід'
    ))

    fig.update_layout(
        title="Загальний дохід за пунктами відправлення",
        xaxis_title="Пункт відправлення",
        yaxis_title="Дохід (грн)",
        xaxis=dict(categoryorder="array", categoryarray=df['departure']),
        height=400,
        width=900,
        template="plotly_white"
    )

    return fig.to_html(full_html=False)

def revenue_by_departure(request):
    sort_order = request.GET.get('sort', 'default')

    revenue_data = get_revenue_data()
    df_revenue = prepare_revenue_dataframe(revenue_data, sort_order)

    stats = calculate_revenue_statistics(df_revenue)
    chart_html = create_revenue_chart(df_revenue)

    return render(request, 'myapp/income_by_departure_dash2.html', {
        'chart_html': chart_html,
        'stats': stats,
        'sort_order': sort_order,
    })