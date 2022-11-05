"""Layout elements for pyllelic-web"""

import dash_bootstrap_components as dbc
from dash import html

TITLE = html.H4("Pyllelic-Web")

THEME = dbc.themes.FLATLY

FOOTER = dbc.Row(
    children=[
        dbc.Col(
            html.P(
                children=[
                    "Visit ",
                    html.A(
                        "Bonham Lab",
                        href="http://www.bonhamlab.com",
                        className="card-text",
                    ),
                ],
                className="card-text",
            ),
        ),
        dbc.Col(
            html.P(
                children=[
                    "Designed by ",
                    html.A(
                        "Dr. Andrew J. Bonham",
                        href="https://github.com/Paradoxdruid",
                        className="card-text",
                    ),
                ],
                className="card-text text-right",
            ),
        ),
    ],
    justify="between",
)
