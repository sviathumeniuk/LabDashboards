from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Category10
from django import forms
from myapp.queries.tickets_on_flight import get_ticket_data1

class SortOrderForm(forms.Form):
    SORT_CHOICES = [
        ('asc', 'За зростанням'),
        ('desc', 'За спаданням')
    ]
    sort_order = forms.ChoiceField(choices=SORT_CHOICES, label="Сортування за ціною", required=False)

def process_sort_form(request):
    form = SortOrderForm(request.POST or None, initial={'sort_order': 'asc'})
    sort_order = form.cleaned_data.get('sort_order', 'asc') if form.is_valid() else 'asc'
    return form, sort_order

def calculate_ticket_statistics(df):
    if df.empty:
        return {
            'total_tickets_sold': 0,
            'total_revenue': 0,
            'average_ticket_price': None,
        }
    return {
        'total_tickets_sold': df.shape[0],
        'total_revenue': df['price'].sum(),
        'average_ticket_price': df['price'].mean(),
    }

def create_ticket_chart(df, flight_id):
    if df.empty:
        return None, "<p>Немає даних для побудови графіка.</p>"

    source = ColumnDataSource(data={
        'seatnumber': df['seatnumber'].astype(str).tolist(),
        'price': df['price'].tolist(),
        'passenger': df['passenger__name'].tolist(),
    })

    unique_passengers = df['passenger__name'].unique().tolist()

    p = figure(
        x_range=df['seatnumber'].astype(str).tolist(),
        height=350,
        title=f"Ціни квитків на рейс {flight_id}",
        toolbar_location=None,
        tools=""
    )

    p.vbar(
        x='seatnumber',
        top='price',
        width=0.9,
        source=source,
        legend_field="passenger",
        color=factor_cmap('passenger', palette=Category10[min(len(unique_passengers), 10)], factors=unique_passengers)
    )

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = "Номер місця"
    p.yaxis.axis_label = "Ціна квитка"
    p.title.align = "center"
    p.legend.title = "Пасажир"

    return components(p)

def tickets_on_flight_dash1(request, flight_id):
    form, sort_order = process_sort_form(request)
    df = get_ticket_data1(flight_id, sort_order)
    stats = calculate_ticket_statistics(df)
    script, div = create_ticket_chart(df, flight_id)

    return render(request, 'myapp/tickets_on_flight_dash1.html', {
        'script': script,
        'div': div,
        'form': form,
        'data': df.to_dict(orient='records'),
        'flight_id': flight_id,
        **stats,
    })
