from dash import html
from dash.dependencies import Input, Output
from apps import navigation
import dash
import dash_bootstrap_components as dbc
import csv
from datetime import date

# current date
today = date.today()
# register this page
dash.register_page(
    __name__,
    path="/add_record",
    title="How neural network learns",
    description="How neural network learns",
    image="logo2.png",
)
# layout contains only widget no Logics
layout = html.Div(
    [
        navigation.navbar,
        dbc.Container(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1("Add New Record", className=""),
                        dbc.Input(
                            id="order-date",
                            type="text",
                            placeholder="Order Date",
                            required=True,
                            className="mt-2",
                            value=today,
                            disabled=True,
                        ),
                        dbc.Select(
                            ["East", "West"],
                            id="region",
                            placeholder="---Region---",
                            className="mt-2",
                            required=True,
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
                        html.Div(id="confirmation-message", style={"marginTop": 10}),
                    ],
                    className="",
                )
            ),
            fluid=False,
            className="mt-5 w-50",
        ),
    ]
)


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
