"""Framework-independent SLA snapshot calculation and HTML rendering."""

from datetime import datetime, timezone
from html import escape


def _as_bool(value):
    """Convert a SOAR Text input or native bool to a predictable boolean."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _parse_deadline(value):
    """Parse ISO-like text; a timezone-less value is explicitly treated as UTC."""
    if value is None or not str(value).strip():
        raise ValueError("SLA deadline is required")

    normalized = str(value).strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        deadline = datetime.fromisoformat(normalized)
    except AttributeError:  # Python 3.6 compatibility declared by setup.py.
        formats = (
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        )
        for date_format in formats:
            try:
                deadline = datetime.strptime(normalized, date_format)
                break
            except ValueError:
                continue
        else:
            raise ValueError("Unsupported SLA deadline format")
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)

    return deadline.astimezone(timezone.utc)


def _format_remaining(total_seconds, show_seconds):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if show_seconds:
        return "{0:02d}:{1:02d}:{2:02d}".format(hours, minutes, seconds)
    return "{0:02d}:{1:02d}".format(hours, minutes)


def render_sla_timer(deadline, label=None, show_seconds=False, now=None):
    """Return a static SLA snapshot; this function does not create a live timer."""
    safe_label = escape(str(label), quote=True) if label not in (None, "") else "SLA"
    include_seconds = _as_bool(show_seconds)

    try:
        parsed_deadline = _parse_deadline(deadline)
    except (TypeError, ValueError, OverflowError):
        timer_html = (
            '<span style="display:inline-block; padding:6px 10px; '
            'border:1px solid #da1e28; color:#da1e28; font-weight:bold;">'
            '{0} INVALID</span>'.format(safe_label)
        )
        return {
            "success": False,
            "expired": False,
            "deadline": str(deadline) if deadline is not None else "",
            "remaining_seconds": 0,
            "remaining_text": "00:00:00" if include_seconds else "00:00",
            "html": timer_html,
            "error": "Invalid SLA deadline. Use an ISO-like date/time value.",
            "type": "sla_timer",
        }

    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    else:
        current = current.astimezone(timezone.utc)

    remaining_seconds = max(0, int((parsed_deadline - current).total_seconds()))
    expired = remaining_seconds == 0
    remaining_text = _format_remaining(remaining_seconds, include_seconds)
    state_text = "EXPIRED / {0}".format(remaining_text) if expired else remaining_text
    color = "#da1e28" if expired else "#198038"

    timer_html = (
        '<span style="display:inline-block; padding:6px 10px; border:1px solid {color}; '
        'color:{color}; font-weight:bold; box-sizing:border-box;">{label} {state}</span>'
    ).format(color=color, label=safe_label, state=state_text)

    return {
        "success": True,
        "expired": expired,
        "deadline": parsed_deadline.isoformat(),
        "remaining_seconds": remaining_seconds,
        "remaining_text": remaining_text,
        "html": timer_html,
        "type": "sla_timer",
    }
