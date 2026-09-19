"""Framework-independent HTML pass-through logic."""


def render_html(html: str) -> dict:
    """Return HTML unchanged for SOAR Rich Text rendering tests."""
    return {
        "success": True,
        "html": html,
        "length": len(html),
    }
