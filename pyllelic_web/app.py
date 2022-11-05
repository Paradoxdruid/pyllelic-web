"""Web frontend for pyllelic bisulfite DNA analysis."""

import dash
import dash_bootstrap_components as dbc
from dash import html

from pyllelic_web.layout import FOOTER, THEME, TITLE

app = dash.Dash(__name__, external_stylesheets=[THEME])
app.title = "Pyllelic-Web"
server = app.server
layout_title = TITLE

# ----------------- Main layout -----------------------------

app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(dbc.Col(html.P("Pyllelic-web placeholder"))),
        dbc.Row(dbc.CardFooter(FOOTER)),
    ],
)
