"""Unit tests for the framework-independent echo service."""

import pytest

from fn_test_app.util.echo_service import echo


@pytest.mark.parametrize("text", ["hello", "QRadar SOAR", "Привет", ""])
def test_echo_returns_expected_result(text):
    assert echo(text) == {
        "success": True,
        "input": text,
        "message": "Received: " + text,
    }
