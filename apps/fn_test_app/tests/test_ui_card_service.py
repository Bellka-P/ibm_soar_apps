"""Unit tests for HTML UI card rendering."""

from fn_test_app.util.ui_card_service import render_ui_card


def test_default_values_are_predictable():
    result = render_ui_card()

    assert result["success"] is True
    assert result["type"] == "ui_card"
    assert "—" in result["html"]
    assert result["length"] == len(result["html"])


def test_all_fields_are_rendered():
    result = render_ui_card(
        severity="HIGH",
        status="OPEN",
        level="L2",
        sla="01:42",
        category="Malware",
        technique="T1204.002",
        client="Example Client",
        host="host-01",
        user="pavel",
        source_ip="10.10.10.10",
        events="42",
        start_time="2026-09-22 14:18",
        creation_date="2026-09-22",
        summary="Analysis in progress",
    )

    for expected in (
        "HIGH", "OPEN", "L2", "01:42", "Malware", "T1204.002",
        "Example Client", "host-01", "pavel", "10.10.10.10", "42",
        "2026-09-22 14:18", "2026-09-22", "Analysis in progress",
    ):
        assert expected in result["html"]


def test_all_user_values_are_html_escaped():
    dangerous = '<script>alert("x")</script> & value'
    result = render_ui_card(
        severity=dangerous,
        status=dangerous,
        level=dangerous,
        sla=dangerous,
        category=dangerous,
        technique=dangerous,
        client=dangerous,
        host=dangerous,
        user=dangerous,
        source_ip=dangerous,
        events=dangerous,
        start_time=dangerous,
        creation_date=dangerous,
        summary=dangerous,
    )

    assert "<script>" not in result["html"]
    assert "&lt;script&gt;" in result["html"]
    assert "&quot;x&quot;" in result["html"]
    assert "&amp; value" in result["html"]


def test_russian_text_is_preserved():
    result = render_ui_card(client="Тестовый клиент", summary="Проверка завершена")

    assert "Тестовый клиент" in result["html"]
    assert "Проверка завершена" in result["html"]


def test_empty_summary_uses_fallback():
    result = render_ui_card(summary="")

    assert "Summary / Сводка" in result["html"]
    assert "—" in result["html"]


def test_special_characters_are_escaped():
    result = render_ui_card(host="node <one> & 'two' \"three\"")

    assert "node &lt;one&gt; &amp; &#x27;two&#x27;" in result["html"]
    assert "&quot;three&quot;" in result["html"]


def test_missing_fields_do_not_break_table_layout():
    result = render_ui_card(status="OPEN")

    assert result["html"].startswith('<table style="width:100%')
    assert "OPEN" in result["html"]
    assert "Summary / Сводка" in result["html"]
