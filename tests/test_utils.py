"""Unit tests for pyllelic_web.utils"""

from pathlib import Path

from dash import html
from pytest_mock.plugin import MockerFixture

from pyllelic_web import utils


def test_list_all_files(mocker: MockerFixture) -> None:

    mocker.patch(
        "pyllelic_web.utils.Path.glob",
        return_value=[Path("test1.bam"), Path("test2.bam")],
    )

    EXPECTED = html.Ul([html.Li("test1"), html.Li("test2")])

    actual = utils.list_all_files("mock")

    assert repr(actual) == repr(EXPECTED)


# def test_hash_dict(mocker: MockerFixture) -> None:
#     pass
