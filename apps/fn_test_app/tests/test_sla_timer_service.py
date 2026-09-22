"""Unit tests for static SLA timer snapshots."""

from datetime import datetime, timedelta, timezone

from fn_test_app.util.sla_timer_service import render_sla_timer


NOW = datetime(2026, 9, 22, 10, 0, 0, tzinfo=timezone.utc)


def test_future_deadline():
    result = render_sla_timer("2026-09-22T11:42:00+00:00", now=NOW)

    assert result["success"] is True
    assert result["expired"] is False
    assert result["remaining_seconds"] == 6120
    assert result["remaining_text"] == "01:42"


def test_expired_deadline_never_becomes_negative():
    result = render_sla_timer("2026-09-22T09:00:00+00:00", now=NOW)

    assert result["expired"] is True
    assert result["remaining_seconds"] == 0
    assert result["remaining_text"] == "00:00"
    assert "EXPIRED" in result["html"]


def test_timezone_aware_deadline_is_converted_to_utc():
    result = render_sla_timer("2026-09-22T16:00:00+05:00", now=NOW)

    assert result["deadline"] == "2026-09-22T11:00:00+00:00"
    assert result["remaining_seconds"] == 3600


def test_timezone_less_deadline_is_treated_as_utc():
    result = render_sla_timer("2026-09-22 11:00:00", now=NOW)

    assert result["deadline"] == "2026-09-22T11:00:00+00:00"
    assert result["remaining_seconds"] == 3600


def test_invalid_datetime_returns_failure_without_raising():
    result = render_sla_timer("not-a-date", now=NOW)

    assert result["success"] is False
    assert result["remaining_seconds"] == 0
    assert result["type"] == "sla_timer"
    assert "error" in result


def test_show_seconds_true_and_false():
    deadline = NOW + timedelta(hours=1, minutes=42, seconds=15)

    with_seconds = render_sla_timer(deadline.isoformat(), show_seconds="true", now=NOW)
    without_seconds = render_sla_timer(deadline.isoformat(), show_seconds="false", now=NOW)

    assert with_seconds["remaining_text"] == "01:42:15"
    assert without_seconds["remaining_text"] == "01:42"


def test_label_is_html_escaped():
    result = render_sla_timer(
        "2026-09-22T11:00:00+00:00",
        label='<img src=x onerror="alert(1)">',
        now=NOW,
    )

    assert "<img" not in result["html"]
    assert "&lt;img" in result["html"]


def test_never_negative_at_exact_deadline():
    result = render_sla_timer(NOW.isoformat(), now=NOW)

    assert result["remaining_seconds"] == 0
    assert result["expired"] is True
