"""Data processing and visualization for pyllelic-web"""

from functools import partialmethod
from typing import Tuple

from dash import dash_table
from plotly.graph_objects import Figure
from pyllelic import pyllelic, visualization
from tqdm import tqdm

tqdm.__init__ = partialmethod(
    tqdm.__init__, disable=True
)  # Suppress progress bars in console output


def run_pyllelic_and_graph() -> Tuple[dash_table.DataTable, Figure, Figure]:
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
        test_dir="test",
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

    reads_graph = visualization._make_stacked_plotly_fig(data.individual_data)

    return (table, heatmap, reads_graph)
