"""Framework-independent HTML UI card rendering."""

from html import escape


EMPTY_VALUE = "—"


def _text(value, default=EMPTY_VALUE):
    """Return an HTML-safe display value without trusting caller content."""
    if value is None or value == "":
        value = default
    return escape(str(value), quote=True)


def render_ui_card(
    severity=None,
    status=None,
    level=None,
    sla=None,
    category=None,
    technique=None,
    client=None,
    host=None,
    user=None,
    source_ip=None,
    events=None,
    start_time=None,
    creation_date=None,
    summary=None,
):
    """Build a compact, table-based card suitable for SOAR Rich Text tests."""
    values = {
        "severity": _text(severity),
        "status": _text(status),
        "level": _text(level),
        "sla": _text(sla),
        "category": _text(category),
        "technique": _text(technique),
        "client": _text(client),
        "host": _text(host),
        "user": _text(user),
        "source_ip": _text(source_ip),
        "events": _text(events),
        "start_time": _text(start_time),
        "creation_date": _text(creation_date),
        "summary": _text(summary),
    }

    card_html = """<table style="width:100%; border-collapse:collapse; box-sizing:border-box; border:1px solid #8d8d8d; font-family:Arial,sans-serif;">
  <tr>
    <td colspan="2" style="padding:10px 12px; background:#262626; color:#ffffff; border-bottom:1px solid #8d8d8d;">
      <strong>{severity}</strong> | {status} | {level} | SLA {sla} | {category} | {technique}
    </td>
  </tr>
  <tr>
    <td style="width:58%; padding:12px; vertical-align:top; box-sizing:border-box;">
      <table style="width:100%; border-collapse:collapse; box-sizing:border-box;">
        <tr><th style="text-align:left; padding:4px 8px 4px 0;">Client</th><td style="padding:4px 12px 4px 0;">{client}</td><th style="text-align:left; padding:4px 8px 4px 0;">Host</th><td style="padding:4px 0;">{host}</td></tr>
        <tr><th style="text-align:left; padding:4px 8px 4px 0;">User</th><td style="padding:4px 12px 4px 0;">{user}</td><th style="text-align:left; padding:4px 8px 4px 0;">Source IP</th><td style="padding:4px 0;">{source_ip}</td></tr>
        <tr><th style="text-align:left; padding:4px 8px 4px 0;">Events</th><td style="padding:4px 12px 4px 0;">{events}</td><th style="text-align:left; padding:4px 8px 4px 0;">Start time</th><td style="padding:4px 0;">{start_time}</td></tr>
        <tr><th style="text-align:left; padding:4px 8px 4px 0;">Created</th><td colspan="3" style="padding:4px 0;">{creation_date}</td></tr>
      </table>
    </td>
    <td style="width:42%; padding:12px; vertical-align:top; box-sizing:border-box; border-left:1px solid #c6c6c6;">
      <strong>Summary / Сводка</strong>
      <div style="padding-top:8px; white-space:pre-wrap; overflow-wrap:anywhere;">{summary}</div>
    </td>
  </tr>
</table>""".format(**values)

    return {
        "success": True,
        "html": card_html,
        "length": len(card_html),
        "type": "ui_card",
    }
