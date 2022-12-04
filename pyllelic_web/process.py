"""Data processing and visualization for pyllelic-web"""

from functools import lru_cache, partialmethod, wraps
from typing import Any, Callable, Dict, Tuple, Union

from dash import dash_table
from plotly.graph_objects import Figure
from pyllelic import pyllelic, visualization
from tqdm import tqdm

tqdm.__init__ = partialmethod(
    tqdm.__init__, disable=True
)  # Suppress progress bars in console output


def hash_dict(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Transform mutable dictionnary into immutable.
    Useful to be compatible with lru_cache
    See https://stackoverflow.com/questions/6358481/
    """

    class HDict(dict):  # type:ignore[type-arg]
        def __hash__(self) -> int:  # type:ignore[override]
            return hash(frozenset(self.items()))

    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        args = tuple([HDict(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: HDict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return wrapped


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
