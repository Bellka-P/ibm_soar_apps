"""Unit tests for the framework-independent HTML service."""

from fn_test_app.util.html_service import render_html


def test_render_html_returns_html_unchanged():
    html = "<h1>Report</h1><p><strong>Status:</strong> Success</p>"

    assert render_html(html) == {
        "success": True,
        "html": html,
        "length": len(html),
    }


def test_render_html_handles_empty_string():
    assert render_html("") == {
        "success": True,
        "html": "",
        "length": 0,
    }


def test_render_html_preserves_unicode():
    html = "<p>Проверка: успешно ✓</p>"

    assert render_html(html)["html"] == html


def test_render_html_preserves_multiline_content():
    html = """<div>
  <p>First line</p>
  <p>Second line</p>
</div>"""

    assert render_html(html)["html"] == html


def test_render_html_length_matches_input_length():
    html = "<pre>SOAR\n  |\n  v\nApp Host</pre>"

    assert render_html(html)["length"] == len(html)
