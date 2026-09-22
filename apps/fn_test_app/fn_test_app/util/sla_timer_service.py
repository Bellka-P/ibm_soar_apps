"""Framework-independent SLA countdown snapshot logic."""

from datetime import datetime, timezone
from html import escape


def _parse_deadline(value):
    """Parse an ISO-like deadline and normalize it to UTC.

    A deadline without a timezone is intentionally interpreted as UTC for this
    test application.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Invalid SLA deadline format")

    normalized = value.strip()
    if normalized.endswith(("Z", "z")):
        normalized = normalized[:-1] + "+00:00"

    try:
        deadline = datetime.fromisoformat(normalized)
    except (TypeError, ValueError):
        raise ValueError("Invalid SLA deadline format")

    if deadline.tzinfo is None or deadline.utcoffset() is None:
        deadline = deadline.replace(tzinfo=timezone.utc)

    return deadline.astimezone(timezone.utc)


def _show_seconds_enabled(value):
    """Convert the required text input ``true`` or ``false`` to bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    raise ValueError("Show Seconds must be true or false")


def render_sla_timer(sla_deadline, sla_label, sla_show_seconds, now=None):
    """Return a static SLA countdown snapshot.

    ``now`` is injectable for deterministic unit tests. A supplied naive
    ``now`` value follows the same test-app convention and is treated as UTC.
    """
    deadline = _parse_deadline(sla_deadline)
    current = now if now is not None else datetime.now(timezone.utc)
    if current.tzinfo is None or current.utcoffset() is None:
        current = current.replace(tzinfo=timezone.utc)
    current = current.astimezone(timezone.utc)

    show_seconds = _show_seconds_enabled(sla_show_seconds)
    delta_seconds = (deadline - current).total_seconds()
    expired = delta_seconds <= 0
    remaining_seconds = max(0, int(delta_seconds))

    hours, remainder = divmod(remaining_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if expired:
        remaining_text = "00:00"
    elif show_seconds:
        remaining_text = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    else:
        remaining_text = "{:02d}:{:02d}".format(hours, minutes)

    safe_label = escape(str(sla_label), quote=True)
    html = (
        '<span style="font-weight:bold; border:1px solid #999; '
        'padding:4px 8px; border-radius:4px;">{} {}</span>'
    ).format(safe_label, remaining_text)

    return {
        "success": True,
        "expired": expired,
        "deadline": deadline.isoformat(),
        "remaining_seconds": remaining_seconds,
        "remaining_text": remaining_text,
        "html": html,
        "type": "sla_timer",
    }
