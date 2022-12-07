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

    data: pyllelic.GenomicPositionData = _run_pyllelic(OPTIONS)

    table: dash_table.DataTable
    heatmap: Figure
    reads_graph: Figure

    table, heatmap, reads_graph = _create_graphs(data)

    return (table, heatmap, reads_graph)


def _run_pyllelic(OPTIONS: Dict[str, Union[str, int]]) -> pyllelic.GenomicPositionData:
    # ----------------- Data Loading -----------------------------
    config: pyllelic.Config = pyllelic.configure(**OPTIONS)

    # See https://paradoxdruid.github.io/pyllelic/

    files_set = pyllelic.make_list_of_bam_files(config)  # finds bam files

    # Run pyllelic; make take some time depending on number of bam files
    data: pyllelic.GenomicPositionData = pyllelic.pyllelic(
        config=config, files_set=files_set
    )

    return data


def _create_graphs(
    data: pyllelic.GenomicPositionData,
) -> Tuple[dash_table.DataTable, Figure, Figure]:

    table = dash_table.DataTable(
        data.means.to_dict("records"),
        [{"name": i, "id": i} for i in data.means.columns],
        style_table={"overflowX": "auto"},
    )

    heatmap: Figure = visualization._create_heatmap(
        data.means,
        min_values=1,
        width=600,
        height=200,
        title_type="Mean",
        backend="plotly",
    )

    reads_graph: Figure = visualization._make_stacked_plotly_fig(data.individual_data)

    return (table, heatmap, reads_graph)
