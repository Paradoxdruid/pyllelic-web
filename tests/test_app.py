"""Unit tests for pyllelic_web.app"""

from pyllelic_web.app import generate_graphs

from .inputs import EXPECTED_APP_OUTPUT


def test_generate_graphs_zero() -> None:

    EXPECTED = "Container(Div(None))"

    actual = generate_graphs(n_clicks=0)

    assert repr(actual) == EXPECTED


def test_generate_graphs() -> None:

    actual = generate_graphs(n_clicks=1)

    # print(repr(actual))

    assert repr(actual) == EXPECTED_APP_OUTPUT
