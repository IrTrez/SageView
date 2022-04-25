from datetime import datetime, timedelta
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go

from pricewebsocket import priceDataWS


coins = ["XLMBTC", "NANOBTC"]
intervals = ["1m", "15m"]

ws = priceDataWS(coins, intervals)
P = pd.DataFrame()
# P = P.append([{"open":0, "high":0, "low":0, "close":0}])


# creates the Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

coinsDropdown = html.Div([
    html.P('Graph Coin:'),
    dcc.Dropdown(
        id='coinDrop',
        options=coins,
        value=coins[0]
    )
])

botData = html.Div([
    html.H2("Bought in:"),
    html.H4("True"),
    html.H2("Profit Today:"),
    html.H4("3.55%"),
    html.H2("Bought in:"),
    html.H4("True")
])


app.layout = html.Div([
    dbc.Row([
        dbc.Col([
                html.Div(
                    [html.H1("Sage View v1"), coinsDropdown, botData],
                    style={"height": "100vh", "background":"lightgrey"},
                )
            ],
            width=3
        ),

        dbc.Col([
            html.Div([html.H1(f"Graph for :"), dcc.Interval(id='update', interval=1000), html.Div(id='page-content')],
                    style={"height": "100vh", "background":"lightcoral"},
                )], width=9),
    ], className="g-0")
])

@app.callback(
    Output('page-content', 'children'),
    Input('update', 'n_intervals'),
    State('coinDrop', 'value')
)
def updateChart(coin, timeframe="1m", numBars=20):
    global P
    numBars = int(numBars)
    print(ws.updated["1m"])
    if ws.updated["1m"]:
        print(f"update {datetime.now()}")
        update = ws.histData
        ws.updated["1m"] = False

        temp = update[f"XLMBTC_1m"]

        P = pd.concat([P, temp])
    # print(P)
    fig = go.Figure(data=go.Candlestick(x=P.index,
            open=P['open'],
            high=P['high'],
            low=P['low'],
            close=P['close']))

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(yaxis={'side': 'right'})
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    return [dcc.Graph(figure=fig, config={'displayModeBar': False})]


if __name__ == "__main__":
    # starts the server
    app.run_server(debug=True)
