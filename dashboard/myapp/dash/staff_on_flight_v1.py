from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from django import forms
from myapp.queries.staff_on_flight import get_staff_data

class FlightFilterForm(forms.Form):
    min_salary = forms.IntegerField(label="Мінімальна зарплата", required=False)

def process_form(request):
    form = FlightFilterForm(request.POST or None)
    if form.is_valid():
        return form, form.cleaned_data.get('min_salary')
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

def create_salary_chart(df, flight_id):
    if df.empty:
        return None, "<p>Немає даних для побудови графіка.</p>"

    source = ColumnDataSource(data={
        'name': df['name'].tolist(),
        'salaries': df['position__salary'].tolist(),
        'positions': df['position__positionname'].tolist(),
    })

    p = figure(
        x_range=df['name'].tolist(),
        height=600,
        width=800,
        title=f"Зарплати співробітників на рейсі {flight_id}",
        toolbar_location=None,
        tools=""
    )
    p.vbar(x='name', top='salaries', width=0.9, source=source, legend_field="positions", color="navy")
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = "Імена співробітників"
    p.yaxis.axis_label = "Зарплата"
    p.title.align = "center"
    p.legend.title = "Посада"

    return components(p)

def staff_on_flight_dash1(request, flight_id):
    form, min_salary = process_form(request)
    df = get_staff_data(flight_id, min_salary)
    stats = calculate_statistics(df)
    script, div = create_salary_chart(df, flight_id)

    return render(request, 'myapp/staff_on_flight_dash1.html', {
        'script': script,
        'div': div,
        'form': form,
        'data': df.to_dict(orient='records'),
        'flight_id': flight_id,
        **stats,
    })
