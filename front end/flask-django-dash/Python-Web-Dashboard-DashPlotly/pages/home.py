from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from apps import navigation
import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

# register this page
dash.register_page(
    __name__,
    path="/",
    title="Plotly deep learning app",
    description="Deep learning simplified",
    image="logo2.png",
)
# load data from github repository
df = pd.read_csv(
    "https://raw.githubusercontent.com/shamiraty/plotly-dashboard/main/demo2.csv"
)
# descriptive analytics
num_items = len(df)
max_price = df["TotalPrice"].max()
min_price = df["TotalPrice"].min()
price_difference = max_price - min_price

# plot1
fig1 = {
    "data": [{"type": "bar", "x": df["OrderDate"], "y": df["UnitPrice"]}],
    "layout": {
        "title": {
            "text": "Figure1: UnitPrice by Date",
            "x": 0.5,  # Center the title horizontally
            "y": 0.9,  # Adjust the vertical position of the title
            "xanchor": "center",
            "yanchor": "top",
            "bgcolor": "rgba(0, 0, 0, 0)",  # Set title background color to transparent
        }
    },
}
# plot2
fig2 = go.Figure(
    data=[go.Box(x=df["City"], y=df["Category"])],
    layout=go.Layout(
        title=go.layout.Title(text="Figure2: Categories by City"),
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Set plot background color to transparent
        paper_bgcolor="rgba(0, 0, 0, 0)",  # Set paper background color to transparent
    ),
)
# plot3
fig3 = px.area(df, x="City", y="TotalPrice", title="Figure3: Total-Price by City")
fig3.update_layout(
    plot_bgcolor="rgba(0, 0, 0, 0)",  # Set plot background color to transparent
    paper_bgcolor="rgba(0, 0, 0, 0)",  # Set paper background color to transparent
)
# layout
layout = html.Div(
    children=[
        navigation.navbar,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Alert(
                                            html.H5("Stock Items"),
                                            className="bg-primary text-white",
                                        ),
                                        html.P(
                                            "Products,UnitPrice,Total price",
                                            className="text-primary",
                                        ),
                                        html.H6(
                                            "Number of Items in Stock",
                                            className="card-title",
                                        ),
                                        html.H2(
                                            f"{num_items} items", className="card-text"
                                        ),
                                    ],
                                    className="card shadow  ",
                                )
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Alert(
                                            html.H5("Max Price"),
                                            className="bg-primary text-white",
                                        ),
                                        html.P(
                                            "Most High frequency Total-Price",
                                            className="text-primary",
                                        ),
                                        html.H6("Price USD", className="card-title"),
                                        html.H2(
                                            f"${max_price:.2f}", className="card-text"
                                        ),
                                    ],
                                    className="card shadow",
                                )
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Alert(
                                            html.H5("Min Price"),
                                            className="bg-primary text-white",
                                        ),
                                        html.P(
                                            "Most lower frequency TotalPrice",
                                            className="text-primary",
                                        ),
                                        html.H6("Price USD", className="card-title"),
                                        html.H2(
                                            f"${min_price:.2f}", className="card-text"
                                        ),
                                    ],
                                    className="card shadow",
                                )
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Alert(
                                            html.H5("Price Deviation"),
                                            className="bg-primary text-white",
                                        ),
                                        html.P(
                                            "Deviation btn Max and Min Total-Price",
                                            className="text-primary",
                                        ),
                                        html.H6("Price USD", className="card-title"),
                                        html.H2(
                                            f"${price_difference:.2f}",
                                            className="card-text",
                                        ),
                                    ],
                                    className="card shadow",
                                )
                            ),
                            width=3,
                        ),
                    ],
                    className="mt-5",
                ),
                dbc.Alert(
                    "Figure 1,2,3: Data exploration can be divided into data preprocessing and data visualization. For data preprocessing, we focus on four methods: univariate analysis, missing value treatment, outlier treatment, and collinearity treatment.",
                    id="alert-fade",
                    dismissable=True,
                    is_open=True,
                    className="alert-warning mt-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card([dcc.Graph(figure=fig1)], className="m-2")),
                        dbc.Col(dbc.Card([dcc.Graph(figure=fig2)], className="m-2")),
                        dbc.Col(dbc.Card([dcc.Graph(figure=fig3)], className="m-2")),
                    ],
                    className="g-0",
                ),
            ],
            fluid=True,
        ),
    ]
)
