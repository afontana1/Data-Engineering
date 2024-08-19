#######
# First Milestone Project: Develop a Stock Ticker
# dashboard that either allows the user to enter
# a ticker symbol into an input box, or to select
# item(s) from a dropdown list, and uses pandas_datareader
# to look up and display stock data on a graph.
######

# ADD A SUBMIT BUTTON TO TAKE ADVANTAGE OF DASH STATE
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web  # requires v0.6.0 or later
from datetime import datetime

app = dash.Dash()

app.layout = html.Div(
    [
        html.H1("Stock Ticker Dashboard"),
        html.Div(
            [
                html.H3("Enter a stock symbol:", style={"paddingRight": "30px"}),
                dcc.Input(
                    id="my_ticker_symbol",
                    value="TSLA",  # sets a default value
                    style={"fontSize": 24, "width": 75},
                ),
            ],
            style={"display": "inline-block", "verticalAlign": "top"},
        ),
        html.Div(
            [
                html.H3("Select start and end dates:"),
                dcc.DatePickerRange(
                    id="my_date_picker",
                    min_date_allowed=datetime(2015, 1, 1),
                    max_date_allowed=datetime.today(),
                    start_date=datetime(2018, 1, 1),
                    end_date=datetime.today(),
                ),
            ],
            style={"display": "inline-block"},
        ),
        html.Div(
            [
                html.Button(
                    id="submit-button",
                    n_clicks=0,
                    children="Submit",
                    style={"fontSize": 24, "marginLeft": "30px"},
                ),
            ],
            style={"display": "inline-block"},
        ),
        dcc.Graph(id="my_graph", figure={"data": [{"x": [1, 2], "y": [3, 1]}]}),
    ]
)


@app.callback(
    Output("my_graph", "figure"),
    [Input("submit-button", "n_clicks")],
    [
        State("my_ticker_symbol", "value"),
        State("my_date_picker", "start_date"),
        State("my_date_picker", "end_date"),
    ],
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], "%Y-%m-%d")
    end = datetime.strptime(end_date[:10], "%Y-%m-%d")
    df = web.DataReader(stock_ticker, "iex", start, end)
    fig = {"data": [{"x": df.index, "y": df.close}], "layout": {"title": stock_ticker}}
    return fig


if __name__ == "__main__":
    app.run_server()
