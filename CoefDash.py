import pandas as pd

import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

coeff = pd.read_csv('https://raw.githubusercontent.com/bors1n/PlotlyDashCoeff/main/coeff_public.csv')

divisions = coeff.divisions_pub.unique().tolist()
options = [{"label": division, "value": division} for division in divisions]

app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H4('Коэффициент сезонности'),

    dcc.Graph(id="time-series-chart"),

    html.P("Выбор категории:"),

    dcc.Dropdown(
        id="ticker",
        options=coeff.category_name.unique(),
        value="Смартфон",
        clearable=False,
    ),

    html.P("Выбор территории:"),
    dcc.Checklist(
        options=options,
        inline=True,
        value=divisions,
        id='checklist',
    )
])

@app.callback(
    Output("time-series-chart", "figure"),
    Input("ticker", "value"),
    Input("checklist", "value"))
def display_time_series(ticker, values):
    df = coeff[coeff['category_name'] == ticker]
    df = df[df['divisions_pub'].isin(values)]
    fig = px.line(df, x='date', y='coff_seas', color='divisions_pub')
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)