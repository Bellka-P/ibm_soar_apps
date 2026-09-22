"""Unit tests for JavaScript/sanitizer capability-test markup."""

from fn_test_app.util.javascript_test_service import WARNING, render_javascript_test


def test_returns_html_and_warning():
    result = render_javascript_test()

    assert result["success"] is True
    assert result["html"]
    assert result["warning"] == WARNING
    assert result["type"] == "javascript_capability_test"


def test_contains_expected_capability_markers():
    html = render_javascript_test("full")["html"]

    for marker in (
        'id="js-test"',
        "onclick=",
        "<script>",
        "setInterval",
        "@keyframes",
        "<details",
        "<iframe",
        "<svg",
    ):
        assert marker in html


def test_mode_is_escaped():
    html = render_javascript_test('<script id="mode">bad</script>')["html"]

    assert '<script id="mode">' not in html
    assert "&lt;script id=&quot;mode&quot;&gt;" in html


def test_service_contains_no_backend_execution_helpers():
    code = render_javascript_test.__code__

    assert "eval" not in code.co_names
    assert "exec" not in code.co_names
    assert "subprocess" not in code.co_names
