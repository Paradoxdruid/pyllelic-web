"""Data processing and visualization for pyllelic-web"""

from functools import lru_cache, partialmethod
from typing import Dict, Tuple, Union

from dash import dash_table
from plotly.graph_objects import Figure
from pyllelic import pyllelic, visualization
from tqdm import tqdm

from pyllelic_web.utils import hash_dict

tqdm.__init__ = partialmethod(
    tqdm.__init__, disable=True
)  # Suppress progress bars in console output


@hash_dict
@lru_cache
def run_pyllelic_and_graph(
    OPTIONS: Dict[str, Union[str, int]],
) -> Tuple[dash_table.DataTable, Figure, Figure]:
    # ----------------- Data Loading -----------------------------
    config = pyllelic.configure(**OPTIONS)

    # See https://paradoxdruid.github.io/pyllelic/

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
