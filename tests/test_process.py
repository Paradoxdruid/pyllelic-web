"""Unit tests for pyllelic_web.process"""

from dataclasses import dataclass

from pandas import DataFrame
from pytest_mock.plugin import MockerFixture

from pyllelic_web import process


@dataclass
class MockData:
    means: DataFrame
    individual_data: DataFrame


# ---------- Tests ------------------------------------


def test__create_graphs(mocker: MockerFixture) -> None:

    mocked_viz = mocker.patch("pyllelic_web.process.visualization")
    mocked_table = mocker.patch("pyllelic_web.process.dash_table")

    SAMPLE_DATA = MockData(
        means=DataFrame({"column1": [1, 2, 3, 4]}),
        individual_data=DataFrame({"column1": [1, 2, 3, 4]}),
    )
    _ = process._create_graphs(SAMPLE_DATA)

    mocked_viz._create_heatmap.assert_called_once()
    mocked_viz._make_stacked_plotly_fig.assert_called_once()
    mocked_table.DataTable.assert_called_once()


def test__run_pyllelic(mocker: MockerFixture) -> None:

    mocked_pyllelic = mocker.patch("pyllelic_web.process.pyllelic")

    _ = process._run_pyllelic({"test": "test"})

    mocked_pyllelic.configure.assert_called_once()

    mocked_pyllelic.make_list_of_bam_files.assert_called_once()

    mocked_pyllelic.pyllelic.assert_called_once()


def test_run_pyllelic_and_graph(mocker: MockerFixture) -> None:

    mocked_run = mocker.patch("pyllelic_web.process._run_pyllelic")
    mocked_graph = mocker.patch(
        "pyllelic_web.process._create_graphs", return_value=(1, 2, 3)
    )

    _ = process.run_pyllelic_and_graph({"test": "test"})

    mocked_run.assert_called_once()
    mocked_graph.assert_called_once()
