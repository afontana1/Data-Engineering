import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import dash

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Img(
                                src=dash.get_asset_url("logo2.png"), height="40px"
                            ),
                            dbc.NavbarBrand("⏱ ANALYTICAL DASHBOARD", className="ms-2"),
                        ],
                        width={"size": "auto"},
                    )
                ],
                align="center",
                className="g-0",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Nav(
                                [
                                    dbc.NavItem(dbc.NavLink("Home", href="/")),
                                    # dbc.NavItem(dbc.NavLink("Fundamentals", href="/fundamentals")),
                                    dbc.NavItem(
                                        dbc.DropdownMenu(
                                            children=[
                                                dbc.DropdownMenuItem(
                                                    "Add Record CSV", href="/add_record"
                                                ),
                                                dbc.DropdownMenuItem(
                                                    "DataSet CSV ", href="/data_set"
                                                ),
                                            ],
                                            nav=True,
                                            in_navbar=True,
                                            label="Data Management",
                                        )
                                    ),
                                    dbc.NavItem(
                                        dbc.DropdownMenu(
                                            children=[
                                                dbc.DropdownMenuItem(
                                                    "Hypothesis Testing", header=True
                                                ),
                                                dbc.DropdownMenuItem(
                                                    "Decision Analysis Tool",
                                                    header=True,
                                                ),
                                                dbc.DropdownMenuItem(
                                                    "K Nearest Neighbor", header=True
                                                ),
                                                dbc.DropdownMenuItem(
                                                    "Price Prediction", header=True
                                                ),
                                                dbc.DropdownMenuItem(
                                                    "Regression", href="/machine"
                                                ),
                                            ],
                                            nav=True,
                                            in_navbar=True,
                                            label="Business Prediction",
                                        )
                                    ),
                                ],
                                navbar=True,
                            )
                        ],
                        width={"size": "auto"},
                    )
                ],
                align="center",
            ),
            dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Collapse(
                            dbc.Nav(
                                [
                                    dbc.NavItem(
                                        dbc.NavLink(
                                            html.I(className="bi bi-github"),
                                            href="https://github.com/shamiraty",
                                            external_link=True,
                                        )
                                    ),
                                    dbc.NavItem(
                                        dbc.NavLink(
                                            html.I(className="bi bi bi-twitter"),
                                            href="",
                                            external_link=True,
                                        )
                                    ),
                                    dbc.NavItem(
                                        dbc.NavLink(
                                            html.I(className="bi bi-youtube"),
                                            href="https://www.youtube.com/channel/UCjepDdFYKzVHFiOhsiVVffQ/",
                                            external_link=True,
                                        )
                                    ),
                                    dbc.Input(type="search", placeholder="Search"),
                                    dbc.Button(
                                        "Search",
                                        color="primary",
                                        className="ms-2",
                                        n_clicks=0,
                                    ),
                                ]
                            ),
                            id="navbar-collapse",
                            is_open=False,
                            navbar=True,
                        )
                    )
                ],
                align="center",
            ),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
)


@dash.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
