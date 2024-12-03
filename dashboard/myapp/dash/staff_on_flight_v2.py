from django.shortcuts import render
from ..models import Staff
import pandas as pd
import plotly.express as px
from django import forms
from myapp.queries.staff_on_flight import get_staff_data

class FlightFilterForm(forms.Form):
    min_salary = forms.IntegerField(label="Мінімальна зарплата", required=False)

def process_form(request):
    form = FlightFilterForm(request.POST or None)
    if form.is_valid():
        return form, form.cleaned_data.get('min_salary', None)
    return form, None

def calculate_statistics(df):
    if df.empty:
        return {
            'min_salary_value': None,
            'max_salary_value': None,
            'median_salary_value': None,
            'average_salary_value': None,
        }
    return {
        'min_salary_value': df['position__salary'].min(),
        'max_salary_value': df['position__salary'].max(),
        'median_salary_value': df['position__salary'].median(),
        'average_salary_value': df['position__salary'].mean(),
    }

def create_graph(df, flight_id):
    if df.empty:
        return None
    fig = px.bar(
        df,
        x='name',
        y='position__salary',
        color='position__positionname',
        labels={
            'name': 'Ім\'я співробітника',
            'position__salary': 'Зарплата',
            'position__positionname': 'Посада'
        },
        title=f"Зарплати співробітників на рейсі {flight_id}"
    )
    fig.update_layout(
        height=600,
        width=800,
        title_font_size=18,
        margin=dict(l=40, r=40, t=40, b=40),
    )
    return fig.to_html(full_html=False)

def staff_on_flight_dash2(request, flight_id):
    form, min_salary = process_form(request)
    df = get_staff_data(flight_id, min_salary)
    stats = calculate_statistics(df)
    graph_html = create_graph(df, flight_id)

    return render(request, 'myapp/staff_on_flight_dash2.html', {
        'graph_html': graph_html,
        'form': form,
        'data': df.to_dict(orient='records'),
        'flight_id': flight_id,
        **stats,
    })
