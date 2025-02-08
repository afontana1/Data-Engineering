from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

# machine learning libraries
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error

# import navigation panel from app dir
from apps import navigation

# register this page
dash.register_page(
    __name__,
    path="/machine",
    title="regression",
    description="Deep learning simplified",
    image="logo2.png",
)

# load data from github repository
df = pd.read_csv(
    "https://raw.githubusercontent.com/shamiraty/plotly-dashboard/main/demo2.csv"
)

# delete unnecessary field
df.drop(
    columns=["OrderDate", "Region", "City", "Category", "Product"], axis=1, inplace=True
)
# feature selection
X = df.iloc[:, :-1]  # left last column
y = df.iloc[:, -1]  # take only last column

# feature splitting
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# standardization Mean=0 SD=1
scaler = StandardScaler()

# re-assign feature to standard Normal
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

# features fitting
regression = LinearRegression()
regression.fit(X_train, y_train)

# cross validation
validation_score = cross_val_score(
    regression, X_train, y_train, scoring="neg_mean_squared_error", cv=3
)
y_pred = regression.predict(X_test)

# performance metrics
meansquareerror = mean_squared_error(y_test, y_pred)
meanabsluteerror = mean_absolute_error(y_test, y_pred)
rootmeansquareerror = np.sqrt(meansquareerror)

# correlation coefficients
score = r2_score(y_test, y_pred)

# coefficients Determination
ajustedR = 1 - (1 - score) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)

# equestion line of fit
fig_ = px.scatter(df, x=y_test, y=y_pred, trendline="ols")
# Make the plot background transparent
fig_.update_layout(
    paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent paper background
    plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent plot background
)
# Show grid lines
fig_.update_xaxes(
    showgrid=True, gridcolor="rgba(0, 0, 0, 0.2)"
)  # Adjust grid color and opacity
fig_.update_yaxes(
    showgrid=True, gridcolor="rgba(0, 0, 0, 0.2)"
)  # Adjust grid color and opacity

# BOX PLOT Outliers
# Melt the DataFrame to combine both columns
melted_data = pd.melt(
    df, value_vars=["UnitPrice", "Quantity"], var_name="Feature", value_name="Value"
)
# Create a boxplot using Plotly Express
fig = px.box(
    melted_data,
    x="Feature",
    y="Value",
    title="Outliers Boxplot for UnitPrice and Quantity",
)
fig.update_layout(
    plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent plot background
    paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent paper background
)
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=True)

#   Layout
layout = html.Div(
    children=[
        navigation.navbar,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Alert(
                            "MULTIPLE REGRESSION  ANALYSIS: Quantity and UnitPrice by TotalPrice ",
                            color="light",
                            className="mt-2",
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Alert(
                                                "Correlation Coefficient",
                                                className="bg-primary text-light",
                                            ),
                                            html.P(
                                                "How Strong X influences Y",
                                                className="text-primary",
                                            ),
                                            html.H6("R", className="card-title"),
                                            html.H4(score),
                                        ],
                                        className="mt-3",
                                    ),
                                    className="mt-3",
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Alert("Coefficient Determination"),
                                            html.P(
                                                "The Ratio X influences Y",
                                                className="text-primary",
                                            ),
                                            html.H6(
                                                "R squared in %", className="card-title"
                                            ),
                                            html.H4(ajustedR * 100),
                                        ],
                                        className="mt-3",
                                    ),
                                    className="mt-3",
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Alert("Mean Squared Error"),
                                            html.P("MSE", className="text-primary"),
                                            html.H6("🟢", className="card-title"),
                                            html.H4(meansquareerror),
                                        ],
                                        className="",
                                    ),
                                    className="mt-3",
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Alert("Mean Absolute Error"),
                                            html.P("MAE", className="text-primary"),
                                            html.H6("🟢", className="card-title"),
                                            html.H4(meanabsluteerror),
                                        ],
                                        className="mt-3",
                                    ),
                                    className="mt-3",
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Alert("Root MeanSquared Error"),
                                            html.P("RMSE", className="text-primary"),
                                            html.H6("🟢", className="card-title"),
                                            html.H4(rootmeansquareerror),
                                        ],
                                        className="mt-3",
                                    ),
                                    className="mt-3",
                                ),
                            ],
                            width=4,
                            className="mt-1",
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Alert(
                                            html.H4(
                                                "Line of Best Fit: y = b1x1 + b2x2 + … + bnxn + c."
                                            )
                                        ),
                                        dbc.Card(
                                            html.Div([dcc.Graph(figure=fig_)]),
                                        ),
                                        dbc.Card(
                                            html.Div([dcc.Graph(figure=fig)]),
                                            className="mt-2",
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                className="mt-3",
                            ),
                            width=8,
                            className="mt-1",
                        ),
                    ],
                ),
            ],
            fluid=True,
        ),
    ]
)
