from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from apps import navigation
import dash
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

# register this page
dash.register_page(
    __name__,
    path="/data_set",
    title="dataset",
    description="Deep learning simplified",
    image="logo2.png",
)
# load csv from github repository
df = pd.read_csv(
    "https://raw.githubusercontent.com/shamiraty/plotly-dashboard/main/demo2.csv"
)
columnDefs = [
    {"field": "OrderDate"},
    {"field": "Region"},
    {"field": "City"},
    {"field": "Category"},
    {"field": "Product"},
    {"field": "Quantity"},
    {"field": "UnitPice"},
    {"field": "TotalPrice"},
]
# table
grid = dag.AgGrid(
    id="getting-started-pagination",
    rowData=df.to_dict("records"),
    columnDefs=columnDefs,
    dashGridOptions={
        "pagination": True,
    },
)
layout = html.Div(
    [
        navigation.navbar,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("List of Items from CSV"),
                                        html.P("List of Items from CSV"),
                                        dbc.Col(html.Div([grid])),
                                    ],
                                )
                            ),
                            width=12,
                            className="mt-5",
                        ),
                    ]
                ),
            ]
        ),
    ]
)
