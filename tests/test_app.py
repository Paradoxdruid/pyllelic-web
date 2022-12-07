"""Unit tests for pyllelic_web.app"""

from dash import html

from pyllelic_web.app import generate_graphs

from .inputs import EXPECTED_APP_OUTPUT


def test_generate_graphs_zero() -> None:

    EXPECTED = html.Div()

    actual = generate_graphs(n_clicks=0)

    assert repr(actual) == repr(EXPECTED)


def test_generate_graphs() -> None:

    actual = generate_graphs(n_clicks=1)

    # print(repr(actual))

    assert repr(actual) == EXPECTED_APP_OUTPUT
