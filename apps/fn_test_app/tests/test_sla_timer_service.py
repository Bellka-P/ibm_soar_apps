"""Unit tests for the framework-independent SLA timer service."""

from datetime import datetime, timezone

import pytest

from fn_test_app.util.sla_timer_service import render_sla_timer


NOW = datetime(2026, 9, 22, 13, 0, 0, tzinfo=timezone.utc)


def test_future_deadline():
    result = render_sla_timer("2026-09-22T14:42:15+00:00", "SLA", "true", NOW)

    assert result["success"] is True
    assert result["expired"] is False
    assert result["remaining_seconds"] == 6135
    assert result["remaining_text"] == "01:42:15"


def test_expired_deadline_never_returns_negative_time():
    result = render_sla_timer("2026-09-22T12:00:00+00:00", "SLA", "true", NOW)

    assert result["expired"] is True
    assert result["remaining_seconds"] == 0
    assert result["remaining_text"] == "00:00"


def test_positive_five_offset_is_normalized_to_utc():
    result = render_sla_timer("2026-09-22T18:00:00+05:00", "SLA", "false", NOW)

    assert result["deadline"] == "2026-09-22T13:00:00+00:00"
    assert result["remaining_seconds"] == 0


def test_z_timezone_is_supported():
    result = render_sla_timer("2026-09-22T13:01:00Z", "SLA", "true", NOW)

    assert result["deadline"] == "2026-09-22T13:01:00+00:00"
    assert result["remaining_seconds"] == 60


def test_timezone_less_deadline_is_treated_as_utc():
    result = render_sla_timer("2026-09-22 14:00:00", "SLA", "false", NOW)

    assert result["deadline"] == "2026-09-22T14:00:00+00:00"
    assert result["remaining_seconds"] == 3600


def test_show_seconds_true():
    result = render_sla_timer("2026-09-22T14:42:15Z", "SLA", "true", NOW)

    assert result["remaining_text"] == "01:42:15"


def test_show_seconds_false():
    result = render_sla_timer("2026-09-22T14:42:15Z", "SLA", "false", NOW)

    assert result["remaining_text"] == "01:42"


def test_invalid_deadline_has_clear_error():
    with pytest.raises(ValueError, match="Invalid SLA deadline format"):
        render_sla_timer("not-a-date", "SLA", "false", NOW)


def test_label_is_html_escaped():
    result = render_sla_timer(
        "2026-09-22T14:00:00Z", '<SLA "critical"> &', "false", NOW
    )

    assert "&lt;SLA &quot;critical&quot;&gt; &amp;" in result["html"]
    assert '<SLA "critical"> &' not in result["html"]


def test_remaining_seconds_is_never_negative():
    result = render_sla_timer("2020-01-01T00:00:00Z", "SLA", "false", NOW)

    assert result["remaining_seconds"] >= 0


def test_hours_do_not_wrap_after_24_hours():
    result = render_sla_timer("2026-09-23T16:15:00Z", "SLA", "false", NOW)

    assert result["remaining_text"] == "27:15"
