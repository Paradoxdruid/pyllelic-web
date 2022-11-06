"""Web frontend for pyllelic bisulfite DNA analysis."""

from functools import partialmethod
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
from pyllelic import pyllelic, visualization
from tqdm import tqdm

from pyllelic_web.layout import FOOTER, NAVBAR, PADDING, THEME, TITLE

tqdm.__init__ = partialmethod(
    tqdm.__init__, disable=True
)  # Suppress progress bars in console output

# ----------------- Initialize App --------------------------

app = dash.Dash(__name__, external_stylesheets=[THEME])
app.title = "Pyllelic-Web"
server = app.server
layout_title = TITLE

# ---------------- Helper Functions --------------------------


def list_all_files(folder_name: str) -> html.Ul:
    my_dir = Path(folder_name)
    files = my_dir.glob("*.bam")
    file_names = [each.stem for each in files]
    file_list = html.Ul([html.Li(file) for file in file_names])

    return file_list


# ----------------- Sample Data Loading ---------------------

# See https://paradoxdruid.github.io/pyllelic/

config = pyllelic.configure(  # Specify file and directory locations
    base_path="./assets/",
    prom_file="tert_genome.txt",
    prom_start=1293200,
    prom_end=1296000,
    chrom="5",
    offset=1293000,  # start position of retrieved promoter sequence
    viz_backend="plotly",
    # fname_pattern=r"^[a-zA-Z]+_([a-zA-Z0-9]+)_.+bam$",
    # test_dir="test",
    # results_dir="results",
)

files_set = pyllelic.make_list_of_bam_files(config)  # finds bam files

# Run pyllelic; make take some time depending on number of bam files
data = pyllelic.pyllelic(config=config, files_set=files_set)

# ------------------- Making Graphs and Output ---------------

table = dash_table.DataTable(
    data.means.to_dict("records"),
    [{"name": i, "id": i} for i in data.means.columns],
    style_table={"overflowX": "auto"},
)

heatmap = visualization._create_heatmap(
    data.means,
    min_values=1,
    width=600,
    height=200,
    title_type="Mean",
    backend="plotly",
)

cell_line = data.cell_types[0]

reads_graph = visualization._make_stacked_plotly_fig(data.individual_data)

# ----------------- Main layout -----------------------------

app.layout = dbc.Container(
    fluid=True,
    children=[
        NAVBAR,
        # dbc.Row(dbc.Col(TITLE)),
        dbc.Row(
            dbc.Col(html.P(f"Pyllelic output of {cell_line} test data.")),
            class_name=PADDING,
        ),
        dbc.Row(dbc.Col(list_all_files("./assets/test"))),
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
        dbc.Row(dbc.Col(dcc.Graph(figure=heatmap), width={"offset": 1, "width": 6})),
        dbc.Row(dbc.Col(dcc.Graph(figure=reads_graph))),
        dbc.Row(dbc.CardFooter(FOOTER), class_name=PADDING),
    ],
)
