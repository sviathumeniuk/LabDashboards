from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10
from django import forms
from myapp.queries.tickets_on_flight import get_ticket_data2

class PassengerSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        passengers = kwargs.pop('passengers', [])
        super().__init__(*args, **kwargs)
        self.fields['passenger'].choices = [(p, p) for p in passengers]
    passenger = forms.ChoiceField(label="Обрати пасажира", required=False)

def process_passenger_form(request, passengers):
    passengers = ["Всі пасажири"] + passengers
    form = PassengerSelectionForm(request.POST or None, passengers=passengers)
    selected_passenger = form.cleaned_data.get('passenger', "Всі пасажири") if form.is_valid() else "Всі пасажири"
    return form, selected_passenger

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
        color=Category10[10][0]
    )

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = "Номер місця"
    p.yaxis.axis_label = "Ціна квитка"
    p.title.align = "center"

    return components(p)

def tickets_on_flight_dash2(request, flight_id):
    df = get_ticket_data2(flight_id)
    passengers = df['passenger__name'].unique().tolist()
    form, selected_passenger = process_passenger_form(request, passengers)
    if selected_passenger != "Всі пасажири":
        df = df[df['passenger__name'] == selected_passenger]
    stats = calculate_ticket_statistics(df)
    script, div = create_ticket_chart(df, flight_id)
    return render(request, 'myapp/tickets_on_flight_dash2.html', {
        'script': script,
        'div': div,
        'form': form,
        'data': df.to_dict(orient='records'),
        'flight_id': flight_id,
        **stats,
    })
