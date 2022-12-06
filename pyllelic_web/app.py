"""Web frontend for pyllelic bisulfite DNA analysis."""

from typing import Dict, Union

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from pyllelic_web.layout import FOOTER, NAVBAR, PADDING, THEME
from pyllelic_web.process import run_pyllelic_and_graph

# ----------------- Initialize App --------------------------

app = dash.Dash(__name__, external_stylesheets=[THEME])
app.title = "Pyllelic-Web"
server = app.server

# ---------------- Helper Functions --------------------------


# ---------------- Temporary Fixed Files for Testing ---------

CONFIG_OPTIONS: Dict[str, Union[str, int]] = {
    "base_path": "./assets/",
    "prom_file": "tert_genome.txt",
    "prom_start": 1293200,
    "prom_end": 1296000,
    "chrom": "5",
    "offset": 1293000,
    "viz_backend": "plotly",
    "test_dir": "test",
}

# ----------------- Main layout -----------------------------

app.layout = dbc.Container(
    fluid=True,
    children=[
        NAVBAR,
        dbc.Row(
            dbc.Col(html.P("Pyllelic output of test data.")),
            class_name=PADDING,
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Generate",
                    color="primary",
                    id="submit-button",
                    class_name="me-1",
                    n_clicks=0,
                )
            ),
            class_name=PADDING,
        ),
        dbc.Row(dbc.Col(html.Div(id="output-div"))),
        dbc.Row(dbc.CardFooter(FOOTER), class_name=PADDING),
    ],
)


@app.callback(
    Output(component_id="output-div", component_property="children"),
    [Input("submit-button", "n_clicks")],
)  # type: ignore[misc]
def generate_graphs(n_clicks: int) -> dbc.Container:

    if n_clicks == 0:
        return html.Div()

    else:

        table, heatmap, reads_graph = run_pyllelic_and_graph(CONFIG_OPTIONS)

        return dbc.Container(
            class_name="border border-primary rounded",
            children=[
                dbc.Row(
                    dbc.Col(
                        html.P(
                            "Mean Methylation Data Table",
                        ),
                        width=7,
                    ),
                    justify="center",
                ),
                dbc.Row(dbc.Col(table, width={"offset": 0, "size": 7})),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=heatmap), width={"offset": 1, "width": 6})
                ),
                dbc.Row(dbc.Col(dcc.Graph(figure=reads_graph))),
            ],
        )
