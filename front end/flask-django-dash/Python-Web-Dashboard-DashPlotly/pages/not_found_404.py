from dash import html
import dash
from apps import navigation
import dash_bootstrap_components as dbc

dash.register_page(__name__, title="Page not found")

layout = html.Div(
    children=[
        navigation.navbar,
        dbc.Container(
            [
                dbc.Toast(
                    [html.P("Page not found, Click Back Home", className="mb-0")],
                    header="NOTIFICATION",
                    icon="primary",
                    dismissable=True,
                    is_open=True,
                    className="mt-5",
                ),
                dbc.Button("Go back to Home", size="lg", id="home_btn_404", href="/"),
            ],
            fluid=False,
        ),
    ],
    className="bg",
)
