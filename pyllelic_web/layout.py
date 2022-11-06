"""Layout elements for pyllelic-web"""

import dash_bootstrap_components as dbc
from dash import html

TITLE = html.H4("Pyllelic-Web")

THEME = dbc.themes.SIMPLEX

PADDING = "py-3"

NAVBAR = dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Actions", header=True),
                dbc.DropdownMenuItem("Action 1", href="#"),
                dbc.DropdownMenuItem("Action 2", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Actions",
        ),
    ],
    brand="Pyllelic-Web",
    brand_href="#",
    color="primary",
    dark=True,
    fluid=True,
    class_name="pb-3",
)

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
