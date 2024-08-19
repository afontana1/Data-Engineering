import dash
import dash_bootstrap_components as dbc
from dash import html

# https://bootswatch.com/united/
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
server = app.server

app.layout = html.Div(children=[dash.page_container])


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)


# if __name__ == "__main__":
# app.run_server(debug=True)
# app.run_server(debug=False,host="0.0.0.0",port=8080)
