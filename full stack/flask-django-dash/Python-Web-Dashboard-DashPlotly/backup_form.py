import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import csv


app = dash.Dash(__name__)


@app.callback(
    Output("confirmation-message", "children"),
    Input("submit-button", "n_clicks"),
    Input("order-date", "value"),
    Input("region", "value"),
    Input("city", "value"),
    Input("category", "value"),
    Input("product", "value"),
    Input("quantity", "value"),
    Input("unit-price", "value"),
    Input("total-price", "value"),
)
def update_csv(
    n_clicks,
    order_date,
    region,
    city,
    category,
    product,
    quantity,
    unit_price,
    total_price,
):
    if n_clicks == 0:
        return ""

    if not all(
        [order_date, region, city, category, product, quantity, unit_price, total_price]
    ):
        return "Please fill in all the fields."

    with open("demo.csv", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                order_date,
                region,
                city,
                category,
                product,
                quantity,
                unit_price,
                total_price,
            ]
        )

    return "Data has been added to the 'demo.csv' file."
