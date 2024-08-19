import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import csv

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H1("Data Entry Form"),
                            dbc.Input(
                                id="order-date",
                                type="text",
                                placeholder="Order Date",
                                required=True,
                                className="mt-2",
                            ),
                            dbc.Input(
                                id="region",
                                type="text",
                                placeholder="Region",
                                required=True,
                                className="mt-2",
                            ),
                            dbc.Input(
                                id="city",
                                type="text",
                                placeholder="City",
                                required=True,
                                className="mt-2",
                            ),
                            dbc.Input(
                                id="category",
                                type="text",
                                placeholder="Category",
                                required=True,
                                className="mt-2",
                            ),
                            dbc.Input(
                                id="product",
                                type="text",
                                placeholder="Product",
                                required=True,
                                className="mt-2",
                            ),
                            dbc.Input(
                                id="quantity",
                                type="number",
                                placeholder="Quantity",
                                required=True,
                                className="mt-2",
                            ),
                            dbc.Input(
                                id="unit-price",
                                type="number",
                                placeholder="Unit Price",
                                required=True,
                                className="mt-2",
                            ),
                            dbc.Input(
                                id="total-price",
                                type="number",
                                placeholder="Total Price",
                                required=True,
                                className="mt-2",
                            ),
                            dbc.Button(
                                "Submit",
                                id="submit-button",
                                color="primary",
                                n_clicks=0,
                                className="w-100 mt-2",
                            ),
                            html.Div(
                                id="confirmation-message", style={"marginTop": 10}
                            ),
                        ],
                        className="",
                    )
                ),
            ]
        ),
    ]
)


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

    with open("demo.csv", "a", newline="") as file:
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


if __name__ == "__main__":
    app.run_server(debug=True)
