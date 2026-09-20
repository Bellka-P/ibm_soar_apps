"""Framework-independent logic for named HTML report blocks."""


def build_html_block(block_name: str, html_content: str) -> dict:
    """Return a named HTML block without modifying its content."""
    return {
        "success": True,
        "block": block_name,
        "html": html_content,
        "length": len(html_content),
    }
