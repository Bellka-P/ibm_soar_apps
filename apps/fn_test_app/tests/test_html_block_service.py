"""Unit tests for the framework-independent HTML block service."""

from fn_test_app.util.html_block_service import build_html_block


def test_summary_returns_correct_block():
    assert build_html_block("summary", "<p>Summary</p>")["block"] == "summary"


def test_checklist_returns_correct_block():
    assert build_html_block("checklist", "<ul><li>Done</li></ul>")["block"] == "checklist"


def test_unicode_is_preserved():
    html = "<p>Проверка завершена успешно ✓</p>"

    assert build_html_block("evidence", html)["html"] == html


def test_multiline_html_is_preserved():
    html = """<ul>
  <li>10:00 - Начало</li>
  <li>10:05 - Завершение</li>
</ul>"""

    assert build_html_block("timeline", html)["html"] == html


def test_html_is_returned_without_changes():
    html = '<div style="color: green"><strong>Approved</strong></div>'

    assert build_html_block("recommendations", html)["html"] == html


def test_length_matches_input_html():
    html = "<h2>Evidence</h2><p>10.10.10.10</p>"

    assert build_html_block("evidence", html)["length"] == len(html)


def test_empty_html_has_predictable_result():
    assert build_html_block("summary", "") == {
        "success": True,
        "block": "summary",
        "html": "",
        "length": 0,
    }
