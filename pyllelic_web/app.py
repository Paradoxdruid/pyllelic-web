"""Web frontend for pyllelic bisulfite DNA analysis."""

from pathlib import Path

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


def list_all_files(folder_name: str) -> html.Ul:
    my_dir = Path(folder_name)
    files = my_dir.glob("*.bam")
    file_names = [each.stem for each in files]
    file_list = html.Ul([html.Li(file) for file in file_names])

    return file_list


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

        table, heatmap, reads_graph = run_pyllelic_and_graph()

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
