"""Unit tests for visual-only CSS timer markup."""

from fn_test_app.util.css_timer_service import WARNING, render_css_timer_experiment


def test_returns_html_and_warning():
    result = render_css_timer_experiment()

    assert result["success"] is True
    assert result["html"]
    assert result["warning"] == WARNING
    assert result["type"] == "css_timer_experiment"


def test_contains_css_animation_markers():
    html = render_css_timer_experiment()["html"]

    assert "@keyframes" in html
    assert "animation:" in html
    assert "soarProgress" in html


def test_contains_no_javascript():
    html = render_css_timer_experiment()["html"].lower()

    assert "<script" not in html
    assert "javascript:" not in html
    assert "onclick" not in html
